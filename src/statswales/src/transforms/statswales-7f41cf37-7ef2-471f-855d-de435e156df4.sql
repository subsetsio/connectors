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
    "Duration" AS duration,
    "Availability" AS availability,
    "Notes" AS notes
FROM "statswales-7f41cf37-7ef2-471f-855d-de435e156df4"
