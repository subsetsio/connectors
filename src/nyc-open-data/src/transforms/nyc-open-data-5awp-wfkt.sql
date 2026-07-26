-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "borough",
    "community_district_cd",
    "borough_consultation_total_snap_recipients",
    "borough_consultation_total_snap_households",
    "borough_consultation_total_cash_assistance_recipients",
    "borough_consultation_total_cash_assistance_cases",
    "borough_consultation_total_medicaid_only_enrollees",
    "borough_consultation_total_medicaid_enrollees"
FROM "nyc-open-data-5awp-wfkt"
