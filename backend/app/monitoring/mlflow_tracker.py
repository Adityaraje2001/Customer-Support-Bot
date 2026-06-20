"""MLflow tracking with Databricks Tracking Server integration.

When DATABRICKS_HOST and DATABRICKS_TOKEN are set, logs are sent to the
Databricks-hosted MLflow service.  If either is missing or the connection
fails, tracking is gracefully disabled (all logging calls become no-ops)
and the application continues running normally.

No local SQLite backend is used — tracking is either Databricks or disabled.
"""

import logging
import os
from typing import Any

import mlflow

from app.config.databricks_config import databricks_settings

logger = logging.getLogger(__name__)


class MLflowTracker:
    """Thin wrapper around the MLflow client with Databricks support."""

    def __init__(
        self,
        experiment_name: str | None = None,
        tracking_uri: str | None = None,
    ):
        self.experiment_name = (
            experiment_name or databricks_settings.DATABRICKS_EXPERIMENT_PATH
        )
        self.tracking_uri = tracking_uri  # allow explicit override
        self.tracking_enabled: bool = False
        self.experiment_id: str | None = None
        self._setup()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        """Configure MLflow tracking URI and experiment.

        Priority:
        1. Explicit ``tracking_uri`` passed to constructor.
        2. Databricks env-var configuration.
        3. Tracking disabled with a warning.
        """
        try:
            if self.tracking_uri:
                # Explicit URI override (e.g. for tests)
                mlflow.set_tracking_uri(self.tracking_uri)
                logger.info(
                    "MLflow tracking URI overridden: %s", self.tracking_uri
                )
            elif databricks_settings.is_configured:
                # Inject env vars required by the MLflow Databricks backend
                os.environ["DATABRICKS_HOST"] = databricks_settings.DATABRICKS_HOST  # type: ignore[assignment]
                os.environ["DATABRICKS_TOKEN"] = databricks_settings.DATABRICKS_TOKEN  # type: ignore[assignment]
                mlflow.set_tracking_uri("databricks")
                logger.info(
                    "MLflow tracking URI set to 'databricks' "
                    "(host=%s)",
                    databricks_settings.DATABRICKS_HOST,
                )
            else:
                logger.warning(
                    "Databricks credentials not found. "
                    "Set DATABRICKS_HOST and DATABRICKS_TOKEN to enable "
                    "MLflow tracking. Tracking is DISABLED."
                )
                return  # tracking_enabled stays False

            # Create / connect to the experiment
            mlflow.set_experiment(self.experiment_name)
            experiment = mlflow.get_experiment_by_name(self.experiment_name)

            if experiment:
                self.experiment_id = experiment.experiment_id
                logger.info(
                    "MLflow experiment ready — name=%s, id=%s",
                    experiment.name,
                    experiment.experiment_id,
                )
            else:
                logger.info(
                    "MLflow experiment created — name=%s",
                    self.experiment_name,
                )

            self.tracking_enabled = True

        except Exception as e:
            logger.warning(
                "Failed to initialise MLflow tracking (tracking disabled): %s",
                e,
            )
            self.tracking_enabled = False

    # ------------------------------------------------------------------
    # Startup validation
    # ------------------------------------------------------------------

    def validate_connection(self) -> dict[str, Any]:
        """Verify Databricks connectivity and experiment existence.

        Called during FastAPI lifespan startup.  Returns a status dict
        with details suitable for structured logging.
        """
        status: dict[str, Any] = {
            "tracking_enabled": self.tracking_enabled,
            "databricks_configured": databricks_settings.is_configured,
            "experiment_name": self.experiment_name,
            "experiment_id": self.experiment_id,
            "databricks_host": databricks_settings.DATABRICKS_HOST,
            "connection_verified": False,
        }

        if not self.tracking_enabled:
            status["reason"] = "Tracking was not enabled during setup"
            return status

        try:
            # Active connectivity check — list the experiment to confirm
            # the Databricks API is reachable and the experiment exists.
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                # Attempt to create it
                exp_id = mlflow.create_experiment(self.experiment_name)
                self.experiment_id = exp_id
                status["experiment_id"] = exp_id
                logger.info(
                    "Created missing experiment '%s' (id=%s)",
                    self.experiment_name,
                    exp_id,
                )
            else:
                self.experiment_id = experiment.experiment_id
                status["experiment_id"] = experiment.experiment_id

            status["connection_verified"] = True
            logger.info(
                "Databricks connectivity verified — host=%s, experiment=%s",
                databricks_settings.DATABRICKS_HOST,
                self.experiment_name,
            )
        except Exception as e:
            logger.warning(
                "Databricks connectivity check failed (tracking disabled): %s",
                e,
            )
            self.tracking_enabled = False
            status["tracking_enabled"] = False
            status["reason"] = str(e)

        return status

    # ------------------------------------------------------------------
    # Run management
    # ------------------------------------------------------------------

    def start_run(self, run_name: str | None = None):
        if not self.tracking_enabled:
            return None
        try:
            run = mlflow.start_run(run_name=run_name)
            logger.debug(
                "MLflow run started — run_id=%s", run.info.run_id
            )
            return run
        except Exception as e:
            logger.warning("Failed to start MLflow run: %s", e)
            return None

    def end_run(self) -> None:
        if not self.tracking_enabled:
            return
        try:
            mlflow.end_run()
        except Exception as e:
            logger.warning("Failed to end MLflow run: %s", e)

    # ------------------------------------------------------------------
    # Logging helpers
    # ------------------------------------------------------------------

    def log_param(self, key: str, value: Any) -> None:
        if not self.tracking_enabled:
            return
        try:
            mlflow.log_param(key, value)
        except Exception as e:
            logger.warning("Failed to log param to MLflow: %s", e)

    def log_metric(self, key: str, value: float) -> None:
        if not self.tracking_enabled:
            return
        try:
            mlflow.log_metric(key, value)
        except Exception as e:
            logger.warning("Failed to log metric to MLflow: %s", e)

    def log_evaluation_metrics(self, scores: dict[str, int]) -> None:
        if not self.tracking_enabled:
            return
        for key, value in scores.items():
            self.log_metric(key, float(value))

    # ------------------------------------------------------------------
    # High-level tracking
    # ------------------------------------------------------------------

    def track_chat_interaction(
        self,
        question: str,
        route_selected: str,
        session_id: str,
        user_id: int | None = None,
        retrieved_document_count: int = 0,
        retrieval_latency_ms: float = 0.0,
        llm_latency_ms: float = 0.0,
        total_response_latency_ms: float = 0.0,
        evaluation_latency_ms: float = 0.0,
        response_length: int = 0,
        ticket_created: bool = False,
        evaluation_scores: dict[str, int] | None = None,
    ) -> dict[str, str | None]:
        """Log a complete chat interaction to Databricks MLflow.

        Returns a dict with ``experiment_id`` and ``run_id`` for
        upstream traceability.  Both are ``None`` when tracking is
        disabled.
        """
        metadata: dict[str, str | None] = {
            "experiment_id": None,
            "run_id": None,
        }

        if not self.tracking_enabled:
            return metadata

        try:
            import contextlib

            run = self.start_run(run_name="chat_interaction")
            with run or contextlib.nullcontext():
                # Params
                self.log_param("question", question)
                self.log_param("route_selected", route_selected)
                self.log_param("session_id", session_id)
                if user_id is not None:
                    self.log_param("user_id", user_id)
                self.log_param("ticket_created", ticket_created)

                # Metrics
                self.log_metric(
                    "retrieved_document_count", float(retrieved_document_count)
                )
                self.log_metric("retrieval_latency_ms", retrieval_latency_ms)
                self.log_metric("llm_latency_ms", llm_latency_ms)
                self.log_metric(
                    "total_response_latency_ms", total_response_latency_ms
                )
                self.log_metric("evaluation_latency_ms", evaluation_latency_ms)
                self.log_metric("response_length", float(response_length))

                if evaluation_scores:
                    self.log_evaluation_metrics(evaluation_scores)

                # Additional metadata — experiment_id & run_id
                if run:
                    run_id = run.info.run_id
                    experiment_id = run.info.experiment_id
                    self.log_param("experiment_id", experiment_id)
                    self.log_param("run_id", run_id)
                    metadata["experiment_id"] = experiment_id
                    metadata["run_id"] = run_id
                    logger.info(
                        "Chat interaction tracked — "
                        "experiment_id=%s, run_id=%s",
                        experiment_id,
                        run_id,
                    )
        except Exception as e:
            logger.warning(
                "Failed to track chat interaction with MLflow: %s", e
            )

        return metadata

    # ------------------------------------------------------------------
    # Feedback tracking
    # ------------------------------------------------------------------

    def track_feedback(
        self,
        feedback_type: str,
        route_selected: str,
        session_id: str,
        user_id: int | None = None,
    ) -> None:
        """Log user feedback to Databricks MLflow.

        Creates a dedicated run named ``user_feedback`` so feedback
        metrics can be aggregated separately from chat interactions.
        """
        if not self.tracking_enabled:
            return

        try:
            import contextlib

            run = self.start_run(run_name="user_feedback")
            with run or contextlib.nullcontext():
                # Params
                self.log_param("feedback_type", feedback_type)
                self.log_param("route_selected", route_selected)
                self.log_param("session_id", session_id)
                if user_id is not None:
                    self.log_param("user_id", user_id)

                # Metrics — binary indicators for easy aggregation
                self.log_metric(
                    "feedback_helpful",
                    1.0 if feedback_type == "helpful" else 0.0,
                )
                self.log_metric(
                    "feedback_not_helpful",
                    1.0 if feedback_type == "not_helpful" else 0.0,
                )

                logger.info(
                    "Feedback tracked — type=%s, route=%s",
                    feedback_type,
                    route_selected,
                )
        except Exception as e:
            logger.warning(
                "Failed to track feedback with MLflow: %s", e
            )


mlflow_tracker = MLflowTracker()
