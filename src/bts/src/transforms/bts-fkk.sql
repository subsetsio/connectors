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
    "ORIGIN_CITY_NUM" AS origin_city_num,
    "ORIGIN_CITY_NAME" AS origin_city_name,
    "ORIGIN_COUNTRY_NAME" AS origin_country_name,
    "ORIGIN_STATE_ABR" AS origin_state_abr,
    "ORIGIN_STATE_FIPS" AS origin_state_fips,
    "ORIGIN_STATE_NM" AS origin_state_nm,
    "ORIGIN_WAC" AS origin_wac,
    CAST("PASSENGERS" AS DOUBLE) AS passengers,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fkk"
