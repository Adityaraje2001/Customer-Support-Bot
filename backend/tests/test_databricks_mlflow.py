# test_databricks_mlflow.py

import os
import mlflow

os.environ["DATABRICKS_HOST"] = "https://dbc-5543cbee-ce22.cloud.databricks.com"
os.environ["DATABRICKS_TOKEN"] = "mock-token-12345"

mlflow.set_tracking_uri("databricks")

experiment_name = "/Users/desaiadityaraje@gmail.com/customer-support-agent"

mlflow.set_experiment(experiment_name)

with mlflow.start_run():
    mlflow.log_param("test", "hello")
    mlflow.log_metric("accuracy", 0.99)

print("SUCCESS")