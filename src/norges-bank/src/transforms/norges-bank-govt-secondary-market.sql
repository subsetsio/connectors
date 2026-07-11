-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "ISIN" AS isin,
    "INSTRUMENT_TYPE" AS instrument_type,
    "COUNTERPARTY_AREA" AS counterparty_area,
    "COUNTERPARTY_TYPE" AS counterparty_type,
    "UNIT_MEASURE" AS unit_measure,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "norges-bank-govt-secondary-market"
