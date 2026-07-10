-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "dataset_id",
    "table_id",
    "type",
    strptime("creation_date", '%Y-%m-%d')::DATE AS creation_date,
    strptime("last_modified_date", '%Y-%m-%d')::DATE AS last_modified_date,
    "creation_time",
    "last_modified_time",
    "row_count",
    "size_bytes"
FROM "base-dos-dados-br-bd-metadados--bigquery-tables"
