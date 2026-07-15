-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "epi_year",
    "epi_week",
    "clinical_status",
    "age_groups",
    "count"
FROM "sg-data-d-0d1da54a73733d33e40f662f757af537"
