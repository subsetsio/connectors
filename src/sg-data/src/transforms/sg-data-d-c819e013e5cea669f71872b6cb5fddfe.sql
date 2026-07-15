-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "segment",
    "infocomm_industry_revenue"
FROM "sg-data-d-c819e013e5cea669f71872b6cb5fddfe"
