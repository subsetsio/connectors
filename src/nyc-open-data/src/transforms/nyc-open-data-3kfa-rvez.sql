-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_type",
    "accela",
    "facility_name",
    "address__no" AS address_no,
    "address_st",
    "bo",
    "zip",
    "inspection_date",
    "inspection_type",
    "of_all_violations",
    "of_phh_violations",
    "of_critical_violations",
    "of_general_violations",
    "docket",
    "lat",
    "long",
    "community_board",
    "council_district",
    "census_tract",
    "boroblocklot",
    "bin",
    "nta",
    "nta_code"
FROM "nyc-open-data-3kfa-rvez"
