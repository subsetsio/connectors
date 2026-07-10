-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Antibiotic Class" AS antibiotic_class,
    CAST("Year" AS BIGINT) AS year,
    "Location" AS location,
    "Age" AS age,
    "Sex" AS sex,
    CAST("Rate" AS BIGINT) AS rate
FROM "cdc-533q-q3rp"
