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
    "RECORD_SNOWFALL" AS record_snowfall,
    "RECORD_SNOWFALL_YR" AS record_snowfall_yr,
    "PREV_RECORD_SNOWFALL" AS prev_record_snowfall,
    "PREV_RECORD_SNOWFALL_YR" AS prev_record_snowfall_yr,
    "FIRST_SNOWFALL" AS first_snowfall,
    "FIRST_SNOWFALL_YEAR" AS first_snowfall_year,
    "SECOND_SNOWFALL" AS second_snowfall,
    "SECOND_SNOWFALL_YEAR" AS second_snowfall_year,
    "THIRD_SNOWFALL" AS third_snowfall,
    "THIRD_SNOWFALL_YEAR" AS third_snowfall_year,
    "FOURTH_SNOWFALL" AS fourth_snowfall,
    "FOURTH_SNOWFALL_YEAR" AS fourth_snowfall_year,
    "FIFTH_SNOWFALL" AS fifth_snowfall,
    "FIFTH_SNOWFALL_YEAR" AS fifth_snowfall_year,
    "PROVINCE_CODE" AS province_code,
    "RECORD_BEGIN" AS record_begin,
    "RECORD_END" AS record_end,
    "IDENTIFIER" AS identifier,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ltce-snowfall"
