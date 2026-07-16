-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw crawl fragments can overlap when continuation runs resume; downstream consumers should use the published transform, which deduplicates rows after normalizing missing product versions.
-- caution: Rows are exploded from EUVD's nested product list, so one vulnerability can appear many times across affected vendors, products, and product versions.
-- row reshape: DISTINCT deduplicates overlapping crawl fragments; unnest-equivalent cardinality change is intentional.
SELECT DISTINCT
    "euvd_id",
    "product_name",
    COALESCE("vendor_name", '') AS vendor_name,
    COALESCE("product_version", '') AS product_version
FROM "enisa-affected-products"
