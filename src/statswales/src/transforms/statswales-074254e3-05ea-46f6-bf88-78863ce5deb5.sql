-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Age of mother" AS age_of_mother,
    "Age of baby" AS age_of_baby,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-074254e3-05ea-46f6-bf88-78863ce5deb5"
