-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "Sex" AS sex,
    "Ethnic group" AS ethnic_group,
    "Notes" AS notes
FROM "statswales-596ed3cf-32b4-4b3f-8b1d-5d9a0b8336e2"
