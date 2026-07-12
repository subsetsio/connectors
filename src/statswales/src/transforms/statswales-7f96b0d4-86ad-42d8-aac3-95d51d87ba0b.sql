-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-7f96b0d4-86ad-42d8-aac3-95d51d87ba0b"
