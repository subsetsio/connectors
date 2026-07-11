-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "INSTRUMENT_TYPE" AS instrument_type,
    "UNIT_MEASURE" AS unit_measure,
    "ISIN" AS isin,
    "ISSUE_TYPE" AS issue_type,
    "MATURITY" AS maturity,
    "INSTR" AS instr,
    "DECIMALS" AS decimals,
    "UNIT_MULT" AS unit_mult,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value
FROM "norges-bank-cbc-transactions"
