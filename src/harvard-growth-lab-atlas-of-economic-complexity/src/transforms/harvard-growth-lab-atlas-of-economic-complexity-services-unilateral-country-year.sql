-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country dimension is not a clean list of countries: `ANS` (`country_id` 999, "Undeclared Countries") is a residual bucket absorbing trade that could not be attributed to a reporter, and it carries the source's few negative trade values. Exclude it to aggregate over real countries; keep it for world totals.
-- caution: Unilateral (reporter-side) service trade, not reconciled against partner reports.
SELECT
    "country_id",
    "country_iso3_code",
    "year",
    "export_value",
    "import_value"
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-country-year"
