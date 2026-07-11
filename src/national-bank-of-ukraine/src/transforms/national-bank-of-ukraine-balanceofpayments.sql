-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains monthly, quarterly, and annual balance-of-payments observations in one long table; filter frequency or period before aggregating.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "t023",
    CAST("s181" AS BIGINT) AS s181,
    "tzep",
    "value"
FROM "national-bank-of-ukraine-balanceofpayments"
