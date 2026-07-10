-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Delay columns are all-cause pre-departure delay measures; do not combine them with ATC-only delay tables unless the cause scope is explicit.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "MONTH_NUM" AS month_num,
    "MONTH_MON" AS month_mon,
    "FLT_DATE" AS flt_date,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    CAST("FLT_DEP_1" AS BIGINT) AS flt_dep_1,
    "FLT_DEP_IFR_2" AS flt_dep_ifr_2,
    "DLY_ALL_PRE_2" AS dly_all_pre_2,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-all-pre-departure-delays"
