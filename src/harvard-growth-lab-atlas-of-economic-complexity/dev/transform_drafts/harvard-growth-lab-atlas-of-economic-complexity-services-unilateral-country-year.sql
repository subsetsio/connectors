-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Unilateral (reporter-side) service trade, not reconciled against partner reports.
SELECT
    "country_id",
    "country_iso3_code",
    "year",
    "export_value",
    "import_value"
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-country-year"
