-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PCS" AS pcs,
    "EEC_MEASURE" AS eec_measure,
    "SEX" AS sex,
    "EDUC" AS educ,
    "UNDEREMP" AS underemp,
    "EMPFORM" AS empform,
    "UNEMPDUR" AS unempdur,
    "COMPOHALO" AS compohalo,
    "EMPSTA" AS empsta,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "WKTIME" AS wktime,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-dd-eec-series"
