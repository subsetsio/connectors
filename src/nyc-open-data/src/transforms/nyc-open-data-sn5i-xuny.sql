-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "alert_date",
    "dataset",
    "dataset_name",
    "status",
    "details",
    "resolution_date",
    "resolution"
FROM "nyc-open-data-sn5i-xuny"
