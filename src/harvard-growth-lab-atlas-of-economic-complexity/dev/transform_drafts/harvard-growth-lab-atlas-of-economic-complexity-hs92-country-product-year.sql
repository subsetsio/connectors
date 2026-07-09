-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Product rows at several hierarchy depths are stacked in one table (`product_level` 1/2/4/6 for HS, 1/2/4 for SITC): a level-6 row's value is already contained in its level-4, -2 and -1 ancestors. Filter `product_level` to a single depth before summing export_value/import_value or counting products.
-- caution: Complexity metrics are only defined at some depths: `export_rca` exists only at `product_level` 4, and `pci`/`distance`/`cog` are absent at level 6. Their nulls mean 'not defined at this depth', not 'missing observation'.
SELECT
    "country_id",
    "country_iso3_code",
    "product_id",
    "product_hs92_code",
    "year",
    "export_value",
    "import_value",
    "global_market_share",
    "distance",
    "cog",
    "pci",
    "export_rca",
    "product_level"
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs92-country-product-year"
