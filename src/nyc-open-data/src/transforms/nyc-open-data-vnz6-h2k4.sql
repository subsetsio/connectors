-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("camis_id" AS BIGINT) AS camis_id,
    "license_type",
    CAST("license_code" AS BIGINT) AS license_code,
    "license_category",
    CAST("license_number" AS BIGINT) AS license_number,
    "business_name",
    "trade_name",
    "activity_type",
    strptime("activity_date", '%m/%d/%Y')::DATE AS activity_date,
    "activity",
    "activity_code",
    "activity_notes",
    "address_building_number",
    "address_street_name",
    "secondary_address_street_name",
    "address_city",
    "address_state",
    "address_postcode",
    "boro_code",
    CAST("community_board" AS BIGINT) AS community_board,
    CAST("council_district" AS BIGINT) AS council_district,
    "borough",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("bin" AS BIGINT) AS bin,
    CAST("bbl" AS BIGINT) AS bbl,
    CAST("census_tract_2020" AS BIGINT) AS census_tract_2020,
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-vnz6-h2k4"
