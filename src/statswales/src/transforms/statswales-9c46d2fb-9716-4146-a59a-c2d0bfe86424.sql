-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Ailment" AS ailment,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-9c46d2fb-9716-4146-a59a-c2d0bfe86424"
