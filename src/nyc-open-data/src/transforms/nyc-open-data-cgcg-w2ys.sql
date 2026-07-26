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
    "filing",
    "schedule",
    "pageno",
    "sequenceno",
    "refno",
    "inv_date",
    "date",
    "_name" AS name,
    "c_code",
    "org_ind",
    "strno",
    "strname",
    "apartment",
    "city",
    "state",
    "zip",
    "pay_method",
    "amnt",
    "purposecd",
    "purpose",
    "_explain" AS explain,
    "exemptcd",
    "rr_ind",
    "seg_ind"
FROM "nyc-open-data-cgcg-w2ys"
