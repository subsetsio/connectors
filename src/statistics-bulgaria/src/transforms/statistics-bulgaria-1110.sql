-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "sex",
    "reasons_leaving_job",
    "employment_experience_unempl",
    "unit",
    "value"
FROM "statistics-bulgaria-1110"
