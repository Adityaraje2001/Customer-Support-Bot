"""Databricks configuration for MLflow Tracking Server integration.

Reads environment variables:
    DATABRICKS_HOST            – Databricks workspace URL
    DATABRICKS_TOKEN           – Personal Access Token (PAT)
    DATABRICKS_EXPERIMENT_PATH – MLflow experiment path (default: /Shared/customer-support-agent)
"""

from pydantic_settings import BaseSettings


class DatabricksSettings(BaseSettings):
    """Databricks connection settings sourced from environment variables."""

    DATABRICKS_HOST: str | None = None
    DATABRICKS_TOKEN: str | None = None
    DATABRICKS_EXPERIMENT_PATH: str = "/Users/desaiadityaraje@gmail.com/customer-support-agent"

    @property
    def is_configured(self) -> bool:
        """Return True when both host and token are provided."""
        return bool(self.DATABRICKS_HOST and self.DATABRICKS_TOKEN)

    class Config:
        env_file = ".env"
        extra = "ignore"


databricks_settings = DatabricksSettings()
