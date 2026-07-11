-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: OBS_VALUE contains the instrument identifier value in this table, not a numeric observation measure.
SELECT
    "INSTRUMENT_TYPE" AS instrument_type,
    "ISIN" AS isin,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "ISSUE_DATE" AS issue_date,
    "TICKER" AS ticker,
    "SETTLEMENT" AS settlement,
    "MATURITY" AS maturity
FROM "norges-bank-cbc-instruments"
