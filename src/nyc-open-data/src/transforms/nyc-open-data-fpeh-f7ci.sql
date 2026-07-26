-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "business_legal_name",
    "assumed_names",
    "street",
    "city",
    "borough",
    "postcode",
    "license_type",
    "license_status",
    "license_issue_date",
    "license_expiration_date",
    "latitude",
    "longitude",
    "council_district",
    "community_board",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "_location" AS location
FROM "nyc-open-data-fpeh-f7ci"
