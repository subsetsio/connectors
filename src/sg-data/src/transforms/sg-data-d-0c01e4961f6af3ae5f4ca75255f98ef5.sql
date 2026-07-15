-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "service_levels",
    "target",
    "achieved"
FROM "sg-data-d-0c01e4961f6af3ae5f4ca75255f98ef5"
