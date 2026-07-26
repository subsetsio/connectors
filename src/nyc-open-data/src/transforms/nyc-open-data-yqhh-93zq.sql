-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "election",
    "officecd",
    "candid",
    "canclass",
    "candlast",
    "candfirst",
    "candmi",
    "committee",
    "_name" AS name,
    "c_code",
    "strno",
    "strname",
    "apartment",
    "boroughcd",
    "city",
    "state",
    "zip",
    "occupation",
    "empname",
    "empstrno",
    "empstrname",
    "empcity",
    "empstate",
    "amnt"
FROM "nyc-open-data-yqhh-93zq"
