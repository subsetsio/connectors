-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "decade",
    "age",
    "male",
    "female",
    "male_perct",
    "female_perct"
FROM "fivethirtyeight-unisex-names-aging-curve"
