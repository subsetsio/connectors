-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Service categories are stacked at several `product_level` depths in one table; filter `product_level` to a single depth before summing values.
SELECT
    "product_id",
    "product_services_unilateral_code",
    "year",
    "export_value",
    "import_value",
    "pci",
    "product_level"
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-product-year"
