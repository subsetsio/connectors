-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "FORECAST_TYPE" AS forecast_type,
    CAST("FORECAST_YEAR" AS BIGINT) AS forecast_year,
    "FORECAST_DATE" AS forecast_date,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "norges-bank-liquidity-forecast"
