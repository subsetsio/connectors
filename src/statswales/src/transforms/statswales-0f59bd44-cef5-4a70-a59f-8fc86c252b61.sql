-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Indicator" AS indicator,
    "Local Authority" AS local_authority,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-0f59bd44-cef5-4a70-a59f-8fc86c252b61"
