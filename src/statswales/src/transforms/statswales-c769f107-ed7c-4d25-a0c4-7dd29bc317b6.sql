-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "APGAR score at 5 minutes" AS apgar_score_at_5_minutes,
    "Notes" AS notes
FROM "statswales-c769f107-ed7c-4d25-a0c4-7dd29bc317b6"
