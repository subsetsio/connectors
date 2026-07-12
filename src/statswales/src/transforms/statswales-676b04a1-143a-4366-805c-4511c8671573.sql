-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Year ending", '%d/%m/%Y')::DATE AS year_ending,
    "Area" AS area,
    "National identity" AS national_identity,
    "Notes" AS notes
FROM "statswales-676b04a1-143a-4366-805c-4511c8671573"
