-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Slot adherence columns partition departures by timing category; use one denominator consistently when calculating shares.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH_NUM" AS BIGINT) AS month_num,
    "MONTH_MON" AS month_mon,
    "FLT_DATE" AS flt_date,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    CAST("FLT_DEP_1" AS BIGINT) AS flt_dep_1,
    CAST("FLT_DEP_REG_1" AS BIGINT) AS flt_dep_reg_1,
    CAST("FLT_DEP_OUT_EARLY_1" AS BIGINT) AS flt_dep_out_early_1,
    CAST("FLT_DEP_IN_1" AS BIGINT) AS flt_dep_in_1,
    CAST("FLT_DEP_OUT_LATE_1" AS BIGINT) AS flt_dep_out_late_1,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-atfm-slot-adherence"
