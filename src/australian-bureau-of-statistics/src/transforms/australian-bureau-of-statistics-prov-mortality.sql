-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
-- caution: The model verifier did not nominate a compact key for this wide cross-tabulation; treat rows as source observations unless a later model pass asserts the full dimension key.
SELECT
    "DATAFLOW" AS dataflow,
    CAST("MEASURE" AS BIGINT) AS measure,
    CAST("SEX" AS BIGINT) AS sex,
    "AGE" AS age,
    "REGION" AS region,
    "MONTH_OCCUR" AS month_occur,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment
FROM "australian-bureau-of-statistics-prov-mortality"
