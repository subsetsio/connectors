-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "SEX" AS sex,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "FIRST_NAME" AS first_name,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-prenom"
