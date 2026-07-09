-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A hierarchical codebook: rows at every `product_level` coexist and are linked by `product_parent_id`. Filter `product_level` to get a flat list of products at one depth.
SELECT
    "product_id",
    "product_hs92_code",
    "product_level",
    "product_name",
    "product_name_short",
    "product_parent_id",
    "product_id_hierarchy",
    "show_feasibility",
    "natural_resource",
    "green_product"
FROM "harvard-growth-lab-atlas-of-economic-complexity-product-hs92"
