-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "INSTRUMENT_TYPE" AS instrument_type,
    "UNIT_MEASURE" AS unit_measure,
    CAST("AUCTION_ID" AS BIGINT) AS auction_id,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "DECIMALS" AS decimals,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "TERM_FROM" AS term_from,
    "TERM_TO" AS term_to,
    "AUCTION_TYPE" AS auction_type,
    "ANNOUNCEMENT_DATE" AS announcement_date,
    "FIXED_INTEREST_RATE" AS fixed_interest_rate
FROM "norges-bank-fauction"
