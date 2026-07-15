-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "brand_and_product_name",
    "package_size"
FROM "sg-data-d-6725eed000bf5b3c5d310eb08de0851f"
