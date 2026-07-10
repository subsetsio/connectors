-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure Name" AS measure_name,
    "Measure Date Range" AS measure_date_range
FROM "cms-fa88-6ff2"
