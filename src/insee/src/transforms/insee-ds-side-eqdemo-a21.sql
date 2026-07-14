-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "FREQ" AS freq,
    "SIDE_MEASURE" AS side_measure,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "ACTIVITY" AS activity,
    "LEGAL_FORM" AS legal_form,
    "COMPANY_LEVEL" AS company_level,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-side-eqdemo-a21"
