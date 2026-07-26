-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "parent_boro",
    "parent_block",
    "parent_lot",
    "parent_bbl",
    "sub_lot_number",
    "sub_lot_bbl",
    "effective_tax_year"
FROM "nyc-open-data-ag5u-vnw2"
