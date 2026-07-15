-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_costs_cent_per_kwh",
    "grid_charges_cent_per_kwh",
    "mkt_support_service_fees_cent_per_kwh",
    "power_sys_ops_mkt_admin_fees_cent_per_kwh"
FROM "sg-data-d-b0b8f7a72f94e983fe42038b9aa4a464"
