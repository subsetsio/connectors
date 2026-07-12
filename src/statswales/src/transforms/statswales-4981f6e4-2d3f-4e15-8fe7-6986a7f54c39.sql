-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Age group" AS age_group,
    "Ethnic group" AS ethnic_group,
    "Notes" AS notes
FROM "statswales-4981f6e4-2d3f-4e15-8fe7-6986a7f54c39"
