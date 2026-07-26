-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vote_year",
    "fiscal_year",
    "council_district",
    "project",
    "ballot_price",
    "subproject_cost",
    "brooklyn_borough_president_funding",
    "total_appropriated",
    "number_of_subprojects",
    "agency",
    "noncity",
    "implementing_cbo",
    "description",
    "installation_location",
    "mapping_location",
    "status_summary",
    "postcode",
    "borough",
    "community_board",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-qm5f-frjb"
