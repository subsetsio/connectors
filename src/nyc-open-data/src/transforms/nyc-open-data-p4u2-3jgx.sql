-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sr",
    "request_date",
    "site_street_address",
    "borocode",
    "community_board",
    "block",
    "lot",
    "violation",
    "permit",
    "homeowner_contractor",
    "attempt",
    "violation_issue_date",
    "assigned_date",
    "inspection_date",
    "passfail",
    "reason_for_failure",
    "car_needed_yn",
    "date_results_are_mailed",
    "expedited",
    "vdd",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-p4u2-3jgx"
