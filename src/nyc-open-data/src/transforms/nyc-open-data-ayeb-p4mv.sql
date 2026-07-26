-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "schoolname",
    "number",
    "street",
    "unit",
    "city",
    "state",
    "postcode",
    "latitude",
    "longitude",
    "contact",
    "telephone",
    "email",
    "web",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020",
    "_location" AS location,
    "data_as_of_date"
FROM "nyc-open-data-ayeb-p4mv"
