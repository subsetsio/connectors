-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "family_assistance_cases",
    "safety_net_assistance_cases",
    "_60_mo_converted_to_sn_cases" AS 60_mo_converted_to_sn_cases,
    "total_cash_assistance_cases_citywide"
FROM "nyc-open-data-9jbx-hna8"
