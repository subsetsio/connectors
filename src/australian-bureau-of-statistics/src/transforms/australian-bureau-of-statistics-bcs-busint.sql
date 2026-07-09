-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE" AS measure,
    "IT_EMP_SIZE" AS it_emp_size,
    "ANZSIC_2006" AS anzsic_2006,
    "REGION_CLASS" AS region_class,
    CAST("INNOV_STATUS" AS BIGINT) AS innov_status,
    CAST("ASGS_2016" AS BIGINT) AS asgs_2016,
    "FREQUENCY" AS frequency,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "australian-bureau-of-statistics-bcs-busint"
