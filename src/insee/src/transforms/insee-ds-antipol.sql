-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "NUMBER_EMPL" AS number_empl,
    "COMPARE_TIME" AS compare_time,
    CAST("ENVT_DEPINV" AS BIGINT) AS envt_depinv,
    "ENVT_DOMAIN" AS envt_domain,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "ACTIVITY" AS activity,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-antipol"
