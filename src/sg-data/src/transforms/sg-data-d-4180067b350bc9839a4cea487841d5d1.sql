-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "elderly_pop",
    "town_estate",
    "number"
FROM "sg-data-d-4180067b350bc9839a4cea487841d5d1"
