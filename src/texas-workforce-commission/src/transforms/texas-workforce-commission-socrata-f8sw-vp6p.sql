-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("fips" AS BIGINT) AS fips,
    CAST("reportingdate" AS TIMESTAMP) AS reportingdate,
    "childethnicityhisplatino",
    "childraceamindalanat",
    "childraceasian",
    "childraceblackafriamer",
    "childracehawaiipacific",
    "childracewhite",
    "childracemult",
    "childmale",
    "childfemale",
    "childdisability",
    "childageinfanttoddler",
    "childageprek",
    "childageschage"
FROM "texas-workforce-commission-socrata-f8sw-vp6p"
