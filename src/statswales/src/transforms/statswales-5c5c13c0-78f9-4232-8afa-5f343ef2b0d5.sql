-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Period", '%d/%m/%Y')::DATE AS period,
    "Area" AS area,
    "Accommodation type" AS accommodation_type,
    "Length of stay" AS length_of_stay,
    "Notes" AS notes
FROM "statswales-5c5c13c0-78f9-4232-8afa-5f343ef2b0d5"
