-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("AIRPORT_SEQ_ID" AS BIGINT) AS airport_seq_id,
    CAST("AIRPORT_ID" AS BIGINT) AS airport_id,
    "AIRPORT" AS airport,
    "DISPLAY_AIRPORT_NAME" AS display_airport_name,
    "DISPLAY_AIRPORT_CITY_NAME_FULL" AS display_airport_city_name_full,
    CAST("AIRPORT_WAC_SEQ_ID2" AS BIGINT) AS airport_wac_seq_id2,
    CAST("AIRPORT_WAC" AS BIGINT) AS airport_wac,
    "AIRPORT_COUNTRY_NAME" AS airport_country_name,
    "AIRPORT_COUNTRY_CODE_ISO" AS airport_country_code_iso,
    "AIRPORT_STATE_NAME" AS airport_state_name,
    "AIRPORT_STATE_CODE" AS airport_state_code,
    "AIRPORT_STATE_FIPS" AS airport_state_fips,
    CAST("CITY_MARKET_SEQ_ID" AS BIGINT) AS city_market_seq_id,
    CAST("CITY_MARKET_ID" AS BIGINT) AS city_market_id,
    "DISPLAY_CITY_MARKET_NAME_FULL" AS display_city_market_name_full,
    CAST("CITY_MARKET_WAC_SEQ_ID2" AS BIGINT) AS city_market_wac_seq_id2,
    CAST("CITY_MARKET_WAC" AS BIGINT) AS city_market_wac,
    "LAT_DEGREES" AS lat_degrees,
    "LAT_HEMISPHERE" AS lat_hemisphere,
    "LAT_MINUTES" AS lat_minutes,
    "LAT_SECONDS" AS lat_seconds,
    "LATITUDE" AS latitude,
    "LON_DEGREES" AS lon_degrees,
    "LON_HEMISPHERE" AS lon_hemisphere,
    "LON_MINUTES" AS lon_minutes,
    "LON_SECONDS" AS lon_seconds,
    "LONGITUDE" AS longitude,
    "UTC_LOCAL_TIME_VARIATION" AS utc_local_time_variation,
    "AIRPORT_START_DATE" AS airport_start_date,
    "AIRPORT_THRU_DATE" AS airport_thru_date,
    CAST("AIRPORT_IS_CLOSED" AS BIGINT) AS airport_is_closed,
    CAST("AIRPORT_IS_LATEST" AS BIGINT) AS airport_is_latest
FROM "bts-fll"
