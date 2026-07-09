-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    CAST("LC_FROM" AS BIGINT) AS lc_from,
    CAST("LC_TO" AS BIGINT) AS lc_to,
    CAST("REGION" AS BIGINT) AS region,
    "STATE" AS state,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment,
    "REPORTING_YEAR_START_DAY" AS reporting_year_start_day
FROM "australian-bureau-of-statistics-lc-cm-yr"
