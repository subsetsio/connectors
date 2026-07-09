-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE" AS measure,
    CAST("SEX" AS BIGINT) AS sex,
    CAST("AGE" AS BIGINT) AS age,
    "EDU_AT" AS edu_at,
    "REGION" AS region,
    "FREQ" AS freq,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "australian-bureau-of-statistics-lf-edu"
