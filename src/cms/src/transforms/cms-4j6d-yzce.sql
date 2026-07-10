-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    "Measure Start Quarter" AS measure_start_quarter,
    "Start Date" AS start_date,
    "Measure End Quarter" AS measure_end_quarter,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-4j6d-yzce"
