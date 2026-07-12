-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Number of babies" AS number_of_babies,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-2604676e-4495-4a87-8482-d3eaf8e97a2d"
