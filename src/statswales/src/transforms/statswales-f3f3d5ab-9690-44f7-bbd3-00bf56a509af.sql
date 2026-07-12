-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Ethnic group" AS ethnic_group,
    "Mode of birth" AS mode_of_birth,
    "Notes" AS notes
FROM "statswales-f3f3d5ab-9690-44f7-bbd3-00bf56a509af"
