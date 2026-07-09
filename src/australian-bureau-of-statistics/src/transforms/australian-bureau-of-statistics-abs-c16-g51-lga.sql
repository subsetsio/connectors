-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "AGE" AS age,
    CAST("SEX_ABS" AS BIGINT) AS sex_abs,
    "INDP_C16" AS indp_c16,
    CAST("STATE" AS BIGINT) AS state,
    "REGIONTYPE" AS regiontype,
    CAST("LGA_2016" AS BIGINT) AS lga_2016,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment
FROM "australian-bureau-of-statistics-abs-c16-g51-lga"
