-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Measure Code" AS measure_code,
    "Measure Name" AS measure_name,
    "Score" AS score,
    "Footnote" AS footnote,
    "Measure Date Range" AS measure_date_range
FROM "cms-3xeb-u9wp"
