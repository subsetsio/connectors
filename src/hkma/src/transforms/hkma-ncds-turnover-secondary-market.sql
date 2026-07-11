-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "purchases_ncds_hkd",
    "purchases_ncds_fc",
    "purchases_ncds_total",
    "sales_ncds_hkd",
    "sales_ncds_fc",
    "sales_ncds_total"
FROM "hkma-ncds-turnover-secondary-market"
