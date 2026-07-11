-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is the latest security-level SOMA holdings snapshot, not a full historical panel.
SELECT
    "asOfDate" AS asofdate,
    "cusip",
    "securityType" AS securitytype,
    "maturityDate" AS maturitydate,
    "issuer",
    "coupon",
    "spread",
    CAST("parValue" AS BIGINT) AS parvalue,
    "inflationCompensation" AS inflationcompensation,
    "percentOutstanding" AS percentoutstanding,
    CAST("changeFromPriorWeek" AS BIGINT) AS changefrompriorweek,
    "changeFromPriorYear" AS changefromprioryear,
    "instrumentGroup" AS instrumentgroup
FROM "ny-fed-soma-holdings"
