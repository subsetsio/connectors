-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes country, state/province, county, metro, and other Google geography levels; filter to the intended geography level before comparing or aggregating rows.
-- caution: Percent changes are relative to Google's pre-pandemic baseline for the same geography and category, not absolute visit counts.
SELECT
    "country_region_code",
    "country_region",
    "sub_region_1",
    "sub_region_2",
    "metro_area",
    "iso_3166_2_code",
    "census_fips_code",
    "place_id",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "parks_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline"
FROM "google-community-mobility-reports"
