-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Sex" AS sex,
    "Year" AS year,
    "Age band" AS age_band,
    "Notes" AS notes
FROM "statswales-b488e046-b1ac-4733-84a2-06b64ac4c7d6"
