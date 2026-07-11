-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "REGNET_TOPIC" AS regnet_topic,
    "REGNET_SECTOR" AS regnet_sector,
    "REGION" AS region,
    "HORIZON" AS horizon,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "UNIT_MEASURE" AS unit_measure,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value
FROM "norges-bank-regnet"
