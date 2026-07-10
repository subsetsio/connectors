-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains several related traffic measures in one airport-day row, including total and IFR departure/arrival counts; choose the intended measure before aggregating.
-- caution: The raw source contains duplicate airport-date identity rows, so deduplicate or aggregate by the dimensions relevant to the query before treating rows as unique airport-day facts.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "MONTH_NUM" AS month_num,
    "MONTH_MON" AS month_mon,
    "FLT_DATE" AS flt_date,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    CAST("FLT_DEP_1" AS BIGINT) AS flt_dep_1,
    CAST("FLT_ARR_1" AS BIGINT) AS flt_arr_1,
    CAST("FLT_TOT_1" AS BIGINT) AS flt_tot_1,
    "FLT_DEP_IFR_2" AS flt_dep_ifr_2,
    "FLT_ARR_IFR_2" AS flt_arr_ifr_2,
    "FLT_TOT_IFR_2" AS flt_tot_ifr_2,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-airport-traffic"
