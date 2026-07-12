-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Month" AS month,
    "Entry cohort" AS entry_cohort,
    "Support type" AS support_type,
    "Notes" AS notes
FROM "statswales-c5f57ce9-18c3-4ac2-8164-7e472d86f0c4"
