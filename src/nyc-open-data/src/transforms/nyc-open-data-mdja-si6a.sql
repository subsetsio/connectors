-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "parent_boro",
    "parent_block",
    "parent_lot",
    "parent_bbl",
    "air_lot_number",
    "air_lot_bbl",
    "effective_tax_year"
FROM "nyc-open-data-mdja-si6a"
