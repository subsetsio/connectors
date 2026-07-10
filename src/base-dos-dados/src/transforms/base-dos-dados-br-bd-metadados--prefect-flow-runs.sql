-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "flow_group_id",
    "name",
    "labels",
    "flow_project_name",
    "flow_name",
    "flow_archived",
    "dataset_id",
    "table_id",
    CAST("start_time" AS TIMESTAMP) AS start_time,
    CAST("end_time" AS TIMESTAMP) AS end_time,
    "state",
    "state_message",
    "task_runs",
    "skipped_upload_to_gcs",
    "error_logs"
FROM "base-dos-dados-br-bd-metadados--prefect-flow-runs"
