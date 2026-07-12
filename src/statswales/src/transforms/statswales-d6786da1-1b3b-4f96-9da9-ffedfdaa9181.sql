-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Smoking status" AS smoking_status,
    "Indicator" AS indicator,
    "Notes" AS notes
FROM "statswales-d6786da1-1b3b-4f96-9da9-ffedfdaa9181"
