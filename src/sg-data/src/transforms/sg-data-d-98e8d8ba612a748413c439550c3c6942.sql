-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "epi_year",
    "epi_week",
    "new_admisison_type",
    "count"
FROM "sg-data-d-98e8d8ba612a748413c439550c3c6942"
