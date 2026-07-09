-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Product rows at several hierarchy depths are stacked in one table (`product_level` 1/2/4/6 for HS, 1/2/4 for SITC): a level-6 row's value is already contained in its level-4, -2 and -1 ancestors. Filter `product_level` to a single depth before summing export_value/import_value or counting products.
-- caution: `pci` is absent at `product_level` 6 — the null means product complexity is not defined at that depth.
SELECT
    "product_id",
    "product_hs12_code",
    "year",
    "export_value",
    "import_value",
    "pci",
    "product_level"
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs12-product-year"
