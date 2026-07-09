-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
-- caution: The model verifier did not nominate a compact key for this wide cross-tabulation; treat rows as source observations unless a later model pass asserts the full dimension key.
SELECT
    "DATAFLOW" AS dataflow,
    CAST("MEASURE" AS BIGINT) AS measure,
    CAST("INDEX" AS BIGINT) AS index,
    CAST("TSEST" AS BIGINT) AS tsest,
    CAST("REGION" AS BIGINT) AS region,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_STATUS" AS obs_status,
    "DECIMALS" AS decimals,
    "OBS_COMMENT" AS obs_comment,
    CAST("BASE_PERIOD" AS BIGINT) AS base_period
FROM "australian-bureau-of-statistics-cpi"
