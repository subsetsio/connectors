-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Provider" AS provider,
    "Dwelling" AS dwelling,
    "Bedrooms" AS bedrooms,
    "Notes" AS notes
FROM "statswales-d3ebaef0-a669-4d8a-94f5-cdfbd94feae5"
