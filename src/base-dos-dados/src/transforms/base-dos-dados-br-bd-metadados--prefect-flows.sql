-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_name",
    "flow_group_id",
    "name",
    CAST("created" AS TIMESTAMP) AS created,
    "latest_version",
    CAST("last_update" AS TIMESTAMP) AS last_update,
    "schedule_type",
    "schedule_cron",
    CAST("schedule_start_date" AS TIMESTAMP) AS schedule_start_date,
    "schedule_filters",
    "schedule_adjustments",
    "schedule_labels",
    "schedule_all_parameters",
    "schedule_parameters_dataset_id",
    "schedule_parameters_table_id",
    "schedule_parameters_dbt_alias",
    "schedule_parameters_materialization_mode",
    "schedule_parameters_materialize_after_dump",
    "schedule_parameters_update_metadata"
FROM "base-dos-dados-br-bd-metadados--prefect-flows"
