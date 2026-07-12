-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nw_lsl",
    "type_of_asset",
    "mkwn_l_sl",
    "asset_component",
    "mw_shr_l_sl",
    "asset_metric",
    "value"
FROM "qatar-planning-and-statistics-authority-value-of-assets-additions-to-assets-and-depreciation-by-type-of-asset-banks-statistics0"
