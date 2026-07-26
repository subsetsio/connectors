-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "_2010_census_bureau_fips_county_code" AS 2010_census_bureau_fips_county_code,
    "_2010_nyc_borough_code" AS 2010_nyc_borough_code,
    "_2010_census_tract" AS 2010_census_tract,
    "puma",
    "neighborhood_tabulation_area_ntacode",
    "neighborhood_tabulation_area_nta_name"
FROM "nyc-open-data-8ius-dhrr"
