-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_waste_landfilled"
FROM "sg-data-d-f0ad4d1fb8c2a9089981fd2f3fe07111"
