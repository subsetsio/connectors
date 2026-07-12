-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Visual Acuity" AS visual_acuity,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-2693d070-ab3a-4243-840d-e5ab0d4aba7d"
