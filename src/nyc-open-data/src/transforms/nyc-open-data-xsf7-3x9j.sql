-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "appurtenant_boro",
    "appurtenant_block",
    "appurtenant_lot",
    "appurtenant_bbl",
    "ident",
    "subident",
    "legacy_reuc_number",
    "deleted_flag",
    "effective_tax_year",
    "parid"
FROM "nyc-open-data-xsf7-3x9j"
