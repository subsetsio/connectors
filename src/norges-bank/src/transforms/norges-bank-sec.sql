-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "SECURITY" AS security,
    "UNIT_MEASURE" AS unit_measure,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "MATURITY" AS maturity,
    "ISSUE_DATE" AS issue_date,
    "COUPON" AS coupon,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value
FROM "norges-bank-sec"
