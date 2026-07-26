-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "houseofworship",
    "streetaddress",
    "city",
    "state",
    "postcode",
    "entrydate",
    "permitnumber",
    "dateissue",
    "dateexpiry",
    "permitstatus",
    "permittype",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-bvug-v3mm"
