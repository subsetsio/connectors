-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "ECONOMIC_SPHERE" AS economic_sphere,
    "FLORES_MEASURE" AS flores_measure,
    "LEGAL_FORM_WITH_PUBLIC" AS legal_form_with_public,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-flores-economic-sphere"
