-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "_quarter" AS quarter,
    "_location" AS location,
    "borough",
    "center",
    "incident_date",
    "basis_for_encounter",
    "the_category_of_the_uof",
    "category_and_number_of_injuries",
    "arrested",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-gxfj-gcr2"
