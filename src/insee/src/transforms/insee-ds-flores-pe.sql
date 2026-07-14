-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "FLORES_MEASURE" AS flores_measure,
    CAST("LEGAL_FORM_WITH_PUBLIC" AS BIGINT) AS legal_form_with_public,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "ACTIVITY" AS activity,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-flores-pe"
