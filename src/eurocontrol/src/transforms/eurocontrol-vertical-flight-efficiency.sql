-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly vertical flight efficiency contains climb and descent measures in the same airport-month row; use the phase-specific columns separately when aggregating.
-- caution: The raw source contains duplicate airport-month identity rows, so deduplicate or aggregate by the dimensions relevant to the query before treating rows as unique airport-month facts.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH_NUM" AS BIGINT) AS month_num,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    "MONTH_MON" AS month_mon,
    "AIRPORT_NAME" AS airport_name,
    CAST("NBR_FLIGHTS_DESCENT" AS BIGINT) AS nbr_flights_descent,
    CAST("TOT_DIST_LEVEL_NM_DESCENT" AS DOUBLE) AS tot_dist_level_nm_descent,
    CAST("TOT_DIST_LVL_NM_DESC_BLW_70" AS DOUBLE) AS tot_dist_lvl_nm_desc_blw_70,
    CAST("TOT_TIME_LEVEL_SECONDS_DESCENT" AS BIGINT) AS tot_time_level_seconds_descent,
    CAST("TOT_TIME_LEVEL_SEC_DESC_BLW_70" AS BIGINT) AS tot_time_level_sec_desc_blw_70,
    CAST("MEDIAN_CDO_ALT" AS BIGINT) AS median_cdo_alt,
    CAST("NBR_CDO_FLIGHTS" AS BIGINT) AS nbr_cdo_flights,
    CAST("NBR_CDO_FLIGHTS_BELOW_7000" AS BIGINT) AS nbr_cdo_flights_below_7000,
    CAST("TOT_DELTA_CO2_KG_DESCENT" AS DOUBLE) AS tot_delta_co2_kg_descent,
    CAST("TOT_DELTA_CO2_KG_DESC_BLW_70" AS DOUBLE) AS tot_delta_co2_kg_desc_blw_70,
    "NBR_FLIGHTS_CLIMB" AS nbr_flights_climb,
    "TOT_DIST_LEVEL_NM_CLIMB" AS tot_dist_level_nm_climb,
    "TOT_DIST_LVL_NM_CLIMB_BLW_100" AS tot_dist_lvl_nm_climb_blw_100,
    "TOT_TIME_LEVEL_SECONDS_CLIMB" AS tot_time_level_seconds_climb,
    "TOT_TIME_LVL_SEC_CLIMB_BLW_100" AS tot_time_lvl_sec_climb_blw_100,
    "MEDIAN_CCO_ALT" AS median_cco_alt,
    "NBR_CCO_FLIGHTS" AS nbr_cco_flights,
    "NBR_CCO_FLIGHTS_BELOW_10000" AS nbr_cco_flights_below_10000,
    "TOT_DELTA_CO2_KG_CLIMB" AS tot_delta_co2_kg_climb,
    "TOT_DELTA_CO2_KG_CLIMB_BLW_100" AS tot_delta_co2_kg_climb_blw_100,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-vertical-flight-efficiency"
