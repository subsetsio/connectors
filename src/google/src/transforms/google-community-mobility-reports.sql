SELECT
    NULLIF(country_region_code, '') AS country_region_code,
    NULLIF(country_region, '')      AS country_region,
    NULLIF(sub_region_1, '')        AS sub_region_1,
    NULLIF(sub_region_2, '')        AS sub_region_2,
    NULLIF(metro_area, '')          AS metro_area,
    NULLIF(iso_3166_2_code, '')     AS iso_3166_2_code,
    NULLIF(census_fips_code, '')    AS census_fips_code,
    NULLIF(place_id, '')            AS place_id,
    CAST(date AS DATE)              AS date,
    TRY_CAST(NULLIF(retail_and_recreation_percent_change_from_baseline, '') AS DOUBLE) AS retail_and_recreation_pct_change,
TRY_CAST(NULLIF(grocery_and_pharmacy_percent_change_from_baseline, '') AS DOUBLE) AS grocery_and_pharmacy_pct_change,
TRY_CAST(NULLIF(parks_percent_change_from_baseline, '') AS DOUBLE) AS parks_pct_change,
TRY_CAST(NULLIF(transit_stations_percent_change_from_baseline, '') AS DOUBLE) AS transit_stations_pct_change,
TRY_CAST(NULLIF(workplaces_percent_change_from_baseline, '') AS DOUBLE) AS workplaces_pct_change,
TRY_CAST(NULLIF(residential_percent_change_from_baseline, '') AS DOUBLE) AS residential_pct_change
FROM "google-community-mobility-reports"
WHERE date IS NOT NULL AND date <> ''
