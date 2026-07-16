-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("QUARTER" AS BIGINT) AS quarter,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "ORIGIN" AS origin,
    "ORIGIN_CITY_NAME" AS origin_city_name,
    CAST("ORIGIN_CITY_NUM" AS BIGINT) AS origin_city_num,
    "ORIGIN_COUNTRY_NAME" AS origin_country_name,
    "ORIGIN_STATE_ABR" AS origin_state_abr,
    "ORIGIN_STATE_FIPS" AS origin_state_fips,
    "ORIGIN_STATE_NM" AS origin_state_nm,
    CAST("ORIGIN_WAC" AS BIGINT) AS origin_wac,
    "DEST" AS dest,
    "DEST_CITY_NAME" AS dest_city_name,
    CAST("DEST_CITY_NUM" AS BIGINT) AS dest_city_num,
    "DEST_STATE_NM" AS dest_state_nm,
    "DEST_STATE_ABR" AS dest_state_abr,
    "DEST_STATE_FIPS" AS dest_state_fips,
    "DEST_COUNTRY_NAME" AS dest_country_name,
    CAST("DEST_WAC" AS BIGINT) AS dest_wac,
    CAST("DOMESTIC" AS DOUBLE) AS domestic,
    CAST("DISTANCE" AS DOUBLE) AS distance,
    CAST("DISTANCE_GROUP" AS BIGINT) AS distance_group,
    CAST("PASSENGERS" AS DOUBLE) AS passengers,
    CAST("FREIGHT" AS DOUBLE) AS freight,
    CAST("MAIL" AS DOUBLE) AS mail,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fkj"
