-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "COMPARE_TIME" AS compare_time,
    "PCS" AS pcs,
    "QUANTILE" AS quantile,
    "SEX" AS sex,
    "ERFS_MEASURE" AS erfs_measure,
    "EMPSTA_ENQ" AS empsta_enq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "TPH" AS tph,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-erfs-non-retropole"
