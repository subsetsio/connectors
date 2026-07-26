-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "item_number",
    "product_name",
    "citystore_exclusive",
    "unit_price",
    "color",
    "size",
    "style",
    "category_name",
    "description"
FROM "nyc-open-data-mqdy-gu73"
