-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "WXO_CITY_CODE" AS wxo_city_code,
    "VIRTUAL_STATION_NAME_E" AS virtual_station_name_e,
    "VIRTUAL_STATION_NAME_F" AS virtual_station_name_f,
    "VIRTUAL_CLIMATE_ID" AS virtual_climate_id,
    "LOCAL_MONTH" AS local_month,
    "LOCAL_DAY" AS local_day,
    "RECORD_PRECIPITATION" AS record_precipitation,
    "RECORD_PRECIPITATION_YR" AS record_precipitation_yr,
    "PREV_RECORD_PRECIPITATION" AS prev_record_precipitation,
    "PREV_RECORD_PRECIPITATION_YR" AS prev_record_precipitation_yr,
    "FIRST_PRECIPITATION" AS first_precipitation,
    "FIRST_PRECIPITATION_YEAR" AS first_precipitation_year,
    "SECOND_PRECIPITATION" AS second_precipitation,
    "SECOND_PRECIPITATION_YEAR" AS second_precipitation_year,
    "THIRD_PRECIPITATION" AS third_precipitation,
    "THIRD_PRECIPITATION_YEAR" AS third_precipitation_year,
    "FOURTH_PRECIPITATION" AS fourth_precipitation,
    "FOURTH_PRECIPITATION_YEAR" AS fourth_precipitation_year,
    "FIFTH_PRECIPITATION" AS fifth_precipitation,
    "FIFTH_PRECIPITATION_YEAR" AS fifth_precipitation_year,
    "PROVINCE_CODE" AS province_code,
    "RECORD_BEGIN" AS record_begin,
    "RECORD_END" AS record_end,
    "IDENTIFIER" AS identifier,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ltce-precipitation"
