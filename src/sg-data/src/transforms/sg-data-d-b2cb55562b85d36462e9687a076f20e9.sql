-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "tons_a_day_per_bil_gdp"
FROM "sg-data-d-b2cb55562b85d36462e9687a076f20e9"
