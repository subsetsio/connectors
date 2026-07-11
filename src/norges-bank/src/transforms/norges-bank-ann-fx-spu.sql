-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "INSTRUMENT_TYPE" AS instrument_type,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    "VALID_FROM" AS valid_from,
    strptime("TRANSACTION_MONTH", '%Y-%m')::DATE AS transaction_month,
    "TRANSACTION_TYPE" AS transaction_type
FROM "norges-bank-ann-fx-spu"
