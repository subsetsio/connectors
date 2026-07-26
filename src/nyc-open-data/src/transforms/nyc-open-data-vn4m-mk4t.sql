-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_publication" AS publication,
    "borough",
    "community_board",
    "priority",
    "tracking_code",
    "request",
    "explanation",
    "response",
    "responded_by",
    "responsible_agency",
    "support_by_1",
    "support_by_2",
    "site_street",
    "cross_street_1",
    "cross_street_2",
    "street_address",
    "block",
    "lot",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-vn4m-mk4t"
