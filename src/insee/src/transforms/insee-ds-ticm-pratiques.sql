-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TICM_MEASURE" AS ticm_measure,
    "SEX" AS sex,
    "FREQ" AS freq,
    "EMPSTA" AS empsta,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "EDUC" AS educ,
    "PCS_ESE" AS pcs_ese,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-ticm-pratiques"
