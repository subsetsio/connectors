-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_index" AS index,
    "admit_date",
    "designation_date",
    "discharge_date",
    "designation_days",
    "los_days",
    "discharge_facility"
FROM "nyc-open-data-q9w2-yi4x"
