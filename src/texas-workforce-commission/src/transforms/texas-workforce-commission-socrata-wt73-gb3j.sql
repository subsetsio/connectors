-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("zipcode" AS BIGINT) AS zipcode,
    CAST("reporting_date" AS TIMESTAMP) AS reporting_date,
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
FROM "texas-workforce-commission-socrata-wt73-gb3j"
