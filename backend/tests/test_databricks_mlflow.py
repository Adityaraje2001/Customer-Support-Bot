import os
import mlflow
from unittest.mock import patch, MagicMock

@patch("mlflow.set_experiment")
@patch("mlflow.start_run")
@patch("mlflow.log_param")
@patch("mlflow.log_metric")
def test_databricks_mlflow(mock_log_metric, mock_log_param, mock_start_run, mock_set_experiment):
    os.environ["DATABRICKS_HOST"] = "https://dbc-5543cbee-ce22.cloud.databricks.com"
    os.environ["DATABRICKS_TOKEN"] = "mock-token-12345"

    mlflow.set_tracking_uri("databricks")

    experiment_name = "/Users/desaiadityaraje@gmail.com/customer-support-agent"

    mlflow.set_experiment(experiment_name)

    mock_run = MagicMock()
    mock_start_run.return_value.__enter__.return_value = mock_run

    with mlflow.start_run():
        mlflow.log_param("test", "hello")
        mlflow.log_metric("accuracy", 0.99)

    mock_set_experiment.assert_called_once_with(experiment_name)
    mock_log_param.assert_called_once_with("test", "hello")
    mock_log_metric.assert_called_once_with("accuracy", 0.99)