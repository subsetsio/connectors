-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly taxi-in additional-time rows are airport-month observations; compare with daily traffic tables only after matching time granularity.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "MONTH_NUM" AS month_num,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    "MONTH_MON" AS month_mon,
    "COMMENT" AS comment,
    "TF" AS tf,
    "VALID_FL" AS valid_fl,
    "NO_REF" AS no_ref,
    "TOTAL_REF_NB_FL" AS total_ref_nb_fl,
    "TOTAL_REF_TIME_MIN" AS total_ref_time_min,
    "TOTAL_ADD_TIME_MIN" AS total_add_time_min,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-taxi-in-additional-time"
