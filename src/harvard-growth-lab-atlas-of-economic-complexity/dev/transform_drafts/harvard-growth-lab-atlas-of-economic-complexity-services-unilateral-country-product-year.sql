-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Service categories are stacked at several `product_level` depths in one table; filter `product_level` to a single depth before summing values.
-- caution: Unilateral (reporter-side) service trade — unlike the goods tables these values are not reconciled against partner reports.
SELECT
    "country_id",
    "country_iso3_code",
    "product_id",
    "product_services_unilateral_code",
    "year",
    "export_value",
    "import_value",
    "global_market_share",
    "product_level"
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-country-product-year"
