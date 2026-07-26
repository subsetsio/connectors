-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "condo_base_boro",
    "condo_base_block",
    "condo_base_lot",
    "condo_base_bbl",
    "condo_number",
    "condo_key",
    "condo_base_bbl_key",
    "unit_boro",
    "unit_block",
    "unit_lot",
    "unit_bbl",
    "unit_designation",
    "floor_text",
    "model",
    "geometry_type",
    "effective_tax_year"
FROM "nyc-open-data-eguu-7ie3"
