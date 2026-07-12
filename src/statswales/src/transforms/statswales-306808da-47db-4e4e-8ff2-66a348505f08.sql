-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area name" AS area_name,
    "Area code" AS area_code,
    "Notes" AS notes
FROM "statswales-306808da-47db-4e4e-8ff2-66a348505f08"
