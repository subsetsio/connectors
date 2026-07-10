-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ATC pre-departure delay is a cause-specific subset and is not additive with the all-cause pre-departure delay table.
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
    "DLY_ATC_PRE_2" AS dly_atc_pre_2,
    "FLT_DEP_3" AS flt_dep_3,
    "DLY_ATC_PRE_3" AS dly_atc_pre_3,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-atc-pre-departure-delays"
