-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes country, state/province, county, metro, and other Google geography levels; filter to the intended geography level before comparing or aggregating rows.
-- caution: Percent changes are relative to Google's pre-pandemic baseline for the same geography and category, not absolute visit counts.
SELECT
    md5(CONCAT_WS('|',
        COALESCE(NULLIF("country_region_code", ''), ''),
        COALESCE(NULLIF("country_region", ''), ''),
        COALESCE(NULLIF("sub_region_1", ''), ''),
        COALESCE(NULLIF("sub_region_2", ''), ''),
        COALESCE(NULLIF("metro_area", ''), ''),
        COALESCE(NULLIF("iso_3166_2_code", ''), ''),
        COALESCE(NULLIF("census_fips_code", ''), ''),
        COALESCE(NULLIF("place_id", ''), '')
    )) AS mobility_region_key,
    NULLIF("country_region_code", '') AS country_region_code,
    NULLIF("country_region", '') AS country_region,
    NULLIF("sub_region_1", '') AS sub_region_1,
    NULLIF("sub_region_2", '') AS sub_region_2,
    NULLIF("metro_area", '') AS metro_area,
    NULLIF("iso_3166_2_code", '') AS iso_3166_2_code,
    NULLIF("census_fips_code", '') AS census_fips_code,
    NULLIF("place_id", '') AS place_id,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    TRY_CAST(NULLIF("retail_and_recreation_percent_change_from_baseline", '') AS DOUBLE) AS retail_and_recreation_pct_change,
    TRY_CAST(NULLIF("grocery_and_pharmacy_percent_change_from_baseline", '') AS DOUBLE) AS grocery_and_pharmacy_pct_change,
    TRY_CAST(NULLIF("parks_percent_change_from_baseline", '') AS DOUBLE) AS parks_pct_change,
    TRY_CAST(NULLIF("transit_stations_percent_change_from_baseline", '') AS DOUBLE) AS transit_stations_pct_change,
    TRY_CAST(NULLIF("workplaces_percent_change_from_baseline", '') AS DOUBLE) AS workplaces_pct_change,
    TRY_CAST(NULLIF("residential_percent_change_from_baseline", '') AS DOUBLE) AS residential_pct_change
FROM "google-community-mobility-reports"
WHERE "date" IS NOT NULL AND "date" <> ''
