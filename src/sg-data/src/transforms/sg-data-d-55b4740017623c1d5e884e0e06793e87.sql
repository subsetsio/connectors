-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "engineering_project",
    "area_reclaimed"
FROM "sg-data-d-55b4740017623c1d5e884e0e06793e87"
