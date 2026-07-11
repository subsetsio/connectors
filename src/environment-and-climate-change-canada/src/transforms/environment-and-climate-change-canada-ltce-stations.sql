-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "VIRTUAL_CLIMATE_ID" AS virtual_climate_id,
    "VIRTUAL_STATION_NAME_E" AS virtual_station_name_e,
    "VIRTUAL_STATION_NAME_F" AS virtual_station_name_f,
    "WXO_CITY_CODE" AS wxo_city_code,
    "ELEMENT_NAME_E" AS element_name_e,
    "CLIMATE_IDENTIFIER" AS climate_identifier,
    "START_DATE" AS start_date,
    "END_DATE" AS end_date,
    "DATA_SOURCE" AS data_source,
    "ENG_STN_NAME" AS eng_stn_name,
    "FRE_STN_NAME" AS fre_stn_name,
    "PROVINCE_CODE" AS province_code,
    "IDENTIFIER" AS identifier,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ltce-stations"
