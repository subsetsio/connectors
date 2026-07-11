-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "ncds_outstanding_hkd",
    "ncds_outstanding_fc",
    "ncds_outstanding_total",
    "of_which_by_ais_hkd",
    "of_which_by_ais_fc",
    "of_which_by_ais_total",
    "of_which_by_pub_hkd",
    "of_which_by_pub_fc",
    "of_which_by_pub_total",
    "proport_outstand_ncds_by_pub_hkd",
    "proport_outstand_ncds_by_pub_fc",
    "proport_outstand_ncds_by_pub_total"
FROM "hkma-ncds-issued-in-hk"
