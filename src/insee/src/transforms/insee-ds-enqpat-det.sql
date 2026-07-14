-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "PCS" AS pcs,
    "QUANTILE" AS quantile,
    "COMPARE_TIME" AS compare_time,
    "QUANTILE_MEASURE" AS quantile_measure,
    "ENQPAT_MEASURE" AS enqpat_measure,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "DEG_URB_UNIT" AS deg_urb_unit,
    "TPH" AS tph,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-enqpat-det"
