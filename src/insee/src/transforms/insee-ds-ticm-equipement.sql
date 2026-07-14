-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TICM_MEASURE" AS ticm_measure,
    "SEX" AS sex,
    "EMPSTA" AS empsta,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "EDUC" AS educ,
    "PCS_ESE" AS pcs_ese,
    "QUANTILE_NIVVIE" AS quantile_nivvie,
    "MUN_DENSITY_LEVEL" AS mun_density_level,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-ticm-equipement"
