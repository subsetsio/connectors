-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "fc_resv_assets_ef",
    "fc_resv_assets_lf",
    "fc_resv_assets_total",
    "unsettle_fx_contracts_ef",
    "unsettle_fx_contracts_lf",
    "unsettle_fx_contracts_total",
    "fc_assets_fx_contracts_ef",
    "fc_assets_fx_contracts_lf",
    "fc_assets_fx_contracts_total"
FROM "hkma-foreign-currency-reserve-assets"
