-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "INSTRUMENT_TYPE" AS instrument_type,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "VALID_FROM" AS valid_from,
    "DELTA_VALUE" AS delta_value,
    CAST("OVERNIGHT_LENDING_RATE" AS DOUBLE) AS overnight_lending_rate,
    "RESERVE_RATE" AS reserve_rate,
    "SIGHT_DEPOSIT_RATE" AS sight_deposit_rate
FROM "norges-bank-ann-kpra"
