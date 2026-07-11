-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "BASE_CUR" AS base_cur,
    "QUOTE_CUR" AS quote_cur,
    "TENOR" AS tenor,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    CAST("CALCULATED" AS BOOLEAN) AS calculated,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "COLLECTION" AS collection,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value
FROM "norges-bank-exr"
