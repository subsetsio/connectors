-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_code",
    "block_number",
    "lot_number",
    "tax_year",
    "owner_name",
    "property_address",
    "granted_reduction_amount",
    "tax_class_code"
FROM "nyc-open-data-4nft-bihw"
