-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Measure Code" AS measure_code,
    "Measure Name" AS measure_name,
    CAST("Score" AS DOUBLE) AS score,
    "Footnote" AS footnote,
    "Measure Date Range" AS measure_date_range
FROM "cms-eda0-92f0"
