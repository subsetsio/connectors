-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("QUARTER" AS BIGINT) AS quarter,
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "UNIQUE_CARRIER_ENTITY" AS unique_carrier_entity,
    "REGION" AS region,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    CAST("CARRIER_GROUP" AS BIGINT) AS carrier_group,
    CAST("CARRIER_GROUP_NEW" AS BIGINT) AS carrier_group_new,
    "AIRPORT_TYPE" AS airport_type,
    CAST("ORIGIN_AIRPORT_ID" AS BIGINT) AS origin_airport_id,
    CAST("ORIGIN_AIRPORT_SEQ_ID" AS BIGINT) AS origin_airport_seq_id,
    CAST("ORIGIN_CITY_MARKET_ID" AS BIGINT) AS origin_city_market_id,
    "ORIGIN" AS origin,
    "ORIGIN_CITY_NAME" AS origin_city_name,
    "ORIGIN_COUNTRY_NAME" AS origin_country_name,
    "ORIGIN_STATE_NM" AS origin_state_nm,
    "ORIGIN_STATE_FIPS" AS origin_state_fips,
    "ORIGIN_STATE_ABR" AS origin_state_abr,
    CAST("ORIGIN_WAC" AS BIGINT) AS origin_wac,
    "SERVICE_CLASS" AS service_class,
    "REV_ACRFT_DEP_SCH_520" AS rev_acrft_dep_sch_520,
    "REV_ACRFT_DEP_PERF_510" AS rev_acrft_dep_perf_510,
    "REV_PAX_ENP_110" AS rev_pax_enp_110,
    "REV_ENP_FREIGHT_217" AS rev_enp_freight_217,
    "REV_ENP_MAIL_219" AS rev_enp_mail_219,
    "NUM_MONTHS" AS num_months,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fkg"
