-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Variant" AS variant,
    "Annual change" AS annual_change,
    "Area" AS area,
    "Component of population change" AS component_of_population_change,
    "Notes" AS notes
FROM "statswales-3e3719b4-746d-4953-8b8b-e4af763bda3e"
