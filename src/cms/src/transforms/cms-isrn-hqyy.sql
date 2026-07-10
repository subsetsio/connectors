-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    "Condition" AS condition,
    "Category" AS category,
    CAST("Score" AS BIGINT) AS score,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-isrn-hqyy"
