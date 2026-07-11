-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains monthly and annual price observations in one long table; filter frequency before comparing or aggregating periods.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    CAST("leveli" AS BIGINT) AS leveli,
    "parent",
    "freq",
    "mcrd081",
    CAST("ku" AS BIGINT) AS ku,
    "mcrk110",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-inflation"
