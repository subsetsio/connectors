-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Geography" AS geography,
    "Sex" AS sex,
    "Age" AS age,
    "Period start" AS period_start,
    "Period end" AS period_end,
    "Notes" AS notes
FROM "statswales-9cb0f00a-3084-42cd-b476-460109d7de08"
