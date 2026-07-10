-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Measure Code" AS measure_code,
    CAST("Score" AS DOUBLE) AS score,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Measure Date Range" AS measure_date_range
FROM "cms-5sqm-2qku"
