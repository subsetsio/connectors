-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Age" AS age,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-eab07ea5-1eb2-481b-8b84-8a5034fc1d6f"
