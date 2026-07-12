-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Age of baby" AS age_of_baby,
    "Breastfeeding Status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-ea7f0635-c9c2-4c5c-9840-be760c1c77cd"
