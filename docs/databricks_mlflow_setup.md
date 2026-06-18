# Databricks MLflow Tracking Server — Setup Guide

This guide explains how to connect the Customer Support Agent backend to a
**Databricks-hosted MLflow Tracking Server** so that all chat-interaction
metrics and parameters are logged centrally.

---

## Prerequisites

| Requirement | Minimum Version |
|---|---|
| Databricks Workspace | Any tier (Community, Standard, Premium) |
| Python `mlflow` package | ≥ 2.11.1 |
| `databricks-sdk` | ≥ 0.20.0 |

Both Python packages are already listed in `requirements.txt`.

---

## 1. Find Your Workspace URL

Your **Databricks Host** is the URL you use to log into your workspace.

1. Open your Databricks workspace in a browser.
2. Copy the URL from the address bar — it looks like:
   ```
   https://adb-1234567890123456.7.azuredatabricks.net
   ```
3. Include the full `https://` prefix. **Do not** add a trailing `/`.

> [!TIP]
> You can also find this under **Workspace Settings → General → Workspace URL**.

---

## 2. Generate a Personal Access Token (PAT)

1. In the Databricks UI, click your **user icon** (top-right) → **User Settings**.
2. Navigate to the **Developer** tab (or **Access Tokens** on older workspaces).
3. Click **Generate New Token**.
4. Set a descriptive comment (e.g. `customer-support-agent-mlflow`) and an
   expiration period (90 days recommended).
5. Click **Generate** and **copy the token immediately** — it will not be shown
   again.

The token looks like:
```
<your-databricks-personal-access-token>
```

> [!CAUTION]
> Treat the PAT like a password. Never commit it to version control. Store it
> only in your `.env` file or a secrets manager.

---

## 3. Configure Environment Variables

Create or update your **`backend/.env`** file:

```dotenv
# --- Databricks MLflow Tracking ---
DATABRICKS_HOST=https://adb-1234567890123456.7.azuredatabricks.net
DATABRICKS_TOKEN=<your-databricks-personal-access-token>
DATABRICKS_EXPERIMENT_PATH=/Shared/customer-support-agent
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABRICKS_HOST` | ✅ | — | Full workspace URL |
| `DATABRICKS_TOKEN` | ✅ | — | Personal Access Token |
| `DATABRICKS_EXPERIMENT_PATH` | ❌ | `/Shared/customer-support-agent` | MLflow experiment path in workspace |

> [!NOTE]
> If both `DATABRICKS_HOST` and `DATABRICKS_TOKEN` are missing or empty, the
> application starts normally with MLflow tracking **disabled**. No data is
> lost — tracking calls become no-ops.

### Docker Compose

The `docker-compose.yml` already reads `backend/.env` via:
```yaml
env_file:
  - ./backend/.env
```
No additional Docker configuration is needed.

---

## 4. Verify Experiment Creation

### Option A — Application Startup Logs

Start the application and check the logs:

```bash
docker-compose up --build
```

Look for one of these log messages:

```
INFO  — MLflow tracking URI set to 'databricks' (host=https://adb-...)
INFO  — MLflow experiment ready — name=/Shared/customer-support-agent, id=123456
INFO  — ✅ Databricks MLflow tracking is ACTIVE
```

If credentials are missing you will see:

```
WARNING — Databricks credentials not found ... Tracking is DISABLED.
WARNING — ⚠️  MLflow tracking is DISABLED — Databricks not configured or unreachable
```

### Option B — Databricks UI

1. Navigate to your Databricks workspace.
2. In the left sidebar, click **Experiments** (under the Machine Learning
   persona) or go to **Workspace → Shared**.
3. Look for the experiment named **`customer-support-agent`** under
   `/Shared/`.
4. Open it — you should see runs with:
   - **Params**: `question`, `route_selected`, `session_id`, `user_id`,
     `ticket_created`
   - **Metrics**: `retrieved_document_count`, `retrieval_latency_ms`,
     `llm_latency_ms`, `total_response_latency_ms`, `response_length`

### Option C — MLflow CLI

```bash
# Set env vars for the CLI session
export DATABRICKS_HOST=https://adb-...
export DATABRICKS_TOKEN=<your-databricks-personal-access-token>

# List experiments
mlflow experiments search --tracking-uri databricks

# List runs in the experiment
mlflow runs list --experiment-id <ID> --tracking-uri databricks
```

---

## 5. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `INVALID_PARAMETER_VALUE: No Experiment with name ...` | First run — experiment doesn't exist yet | The app creates it automatically. Check IAM permissions. |
| `401 Unauthorized` | Token expired or invalid | Generate a new PAT (Section 2). |
| `ConnectionError` / `DNS resolution failed` | Wrong `DATABRICKS_HOST` | Double-check the workspace URL (Section 1). |
| Tracking silently disabled | Env vars not loaded | Ensure `.env` is in `backend/` and `python-dotenv` loads it. |
| `Experiment ... is in 'deleted' state` | Experiment was soft-deleted | Restore it from the Databricks Trash, or change `DATABRICKS_EXPERIMENT_PATH`. |

---

## Architecture Overview

```
┌────────────────────────────────────────────────────┐
│  FastAPI App  (main.py)                            │
│    ├── lifespan: validates tracking at startup     │
│    └── chat.py: calls mlflow_tracker               │
│         └── MLflowTracker  (mlflow_tracker.py)     │
│              ├── reads DatabricksSettings           │
│              │     (databricks_config.py)           │
│              ├── sets tracking_uri = "databricks"   │
│              ├── sets DATABRICKS_HOST/TOKEN env     │
│              └── logs params & metrics via MLflow   │
│                       │                            │
└───────────────────────┼────────────────────────────┘
                        │  HTTPS
                        ▼
          ┌──────────────────────────┐
          │  Databricks Workspace    │
          │  MLflow Tracking Server  │
          │  /Shared/customer-       │
          │   support-agent          │
          └──────────────────────────┘
```

---

## What's NOT Covered (Future Phases)

- Model Registry integration
- Unity Catalog
- Databricks Jobs
- Serving Endpoints
