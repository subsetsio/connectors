-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: OBS_VALUE is an identifier-style calendar value in this table, not a numeric observation measure.
SELECT
    "ISIN" AS isin,
    "MATURITY" AS maturity,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    CAST("VOLUME" AS BIGINT) AS volume,
    "AUCTION_DATE" AS auction_date,
    "SETTLEMENT" AS settlement,
    "AUCTION_TYPE" AS auction_type,
    "ISSUE_TYPE" AS issue_type,
    "LASTUPDATED" AS lastupdated,
    CAST("MATURITYDAYS" AS BIGINT) AS maturitydays,
    "BIDDEADLINE" AS biddeadline,
    "STARTTIME" AS starttime
FROM "norges-bank-cbc-calendar"
