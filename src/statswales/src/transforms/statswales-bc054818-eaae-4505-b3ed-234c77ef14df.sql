-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Mothers weight gain" AS mothers_weight_gain,
    "BMI group" AS bmi_group,
    "Notes" AS notes
FROM "statswales-bc054818-eaae-4505-b3ed-234c77ef14df"
