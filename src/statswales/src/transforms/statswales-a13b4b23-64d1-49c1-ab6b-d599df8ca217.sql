-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area code" AS area_code,
    "Area name" AS area_name,
    "Indicator" AS indicator,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-a13b4b23-64d1-49c1-ab6b-d599df8ca217"
