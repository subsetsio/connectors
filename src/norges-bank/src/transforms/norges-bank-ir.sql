-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "INSTRUMENT_TYPE" AS instrument_type,
    "TENOR" AS tenor,
    "UNIT_MEASURE" AS unit_measure,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "COLLECTION" AS collection,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "CALC_METHOD" AS calc_method
FROM "norges-bank-ir"
