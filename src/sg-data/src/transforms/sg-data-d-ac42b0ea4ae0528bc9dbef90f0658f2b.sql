-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "epi_year",
    "epi_week",
    "status",
    "count"
FROM "sg-data-d-ac42b0ea4ae0528bc9dbef90f0658f2b"
