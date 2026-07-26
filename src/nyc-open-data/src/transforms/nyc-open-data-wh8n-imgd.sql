-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_period",
    "reporting_category",
    "age_group",
    "unique_individuals_or_families"
FROM "nyc-open-data-wh8n-imgd"
