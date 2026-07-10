-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Provider_ID" AS provider_id,
    "Measure" AS measure,
    CAST("Rate" AS DOUBLE) AS rate,
    "Footnote" AS footnote,
    "Start_Quarter" AS start_quarter,
    "End_Quarter" AS end_quarter
FROM "cms-01edb62e-5c45-4f43-8c91-16cba21cbb74"
