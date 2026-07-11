-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "COUNTERPARTY" AS counterparty,
    "UNIT_MEASURE" AS unit_measure,
    CAST("INITIAL_YEAR" AS BIGINT) AS initial_year,
    CAST("MATURITY_MONTH" AS BIGINT) AS maturity_month,
    CAST("MATURITY_YEAR" AS BIGINT) AS maturity_year,
    CAST("START_MONTH" AS BIGINT) AS start_month,
    CAST("START_YEAR" AS BIGINT) AS start_year,
    CAST("TRN" AS BIGINT) AS trn,
    "FREQ" AS freq,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "norges-bank-govt-irs"
