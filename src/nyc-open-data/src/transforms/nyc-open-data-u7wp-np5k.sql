-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "provider_type",
    "site_name",
    "sponsorvendor",
    "geriatric_mental_health_gmh_service_site",
    "site_type",
    "dfta_id",
    "site_address",
    "address_line_2",
    "borough",
    "zip_code",
    "community_district",
    "city_council_district",
    "x_coordinate",
    "y_coordinate",
    "latitude",
    "longitude",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-u7wp-np5k"
