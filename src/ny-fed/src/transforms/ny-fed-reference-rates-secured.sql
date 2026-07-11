-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The SOFRAI type is an index/average series, while SOFR, BGCR, and TGCR are daily rates; compare or aggregate only after filtering to compatible rate types.
SELECT
    "effectiveDate" AS effectivedate,
    "type",
    "percentRate" AS percentrate,
    "percentPercentile1" AS percentpercentile1,
    "percentPercentile25" AS percentpercentile25,
    "percentPercentile75" AS percentpercentile75,
    "percentPercentile99" AS percentpercentile99,
    "volumeInBillions" AS volumeinbillions,
    "targetRateFrom" AS targetratefrom,
    "targetRateTo" AS targetrateto,
    "average30day",
    "average90day",
    "average180day",
    "index",
    "revisionIndicator" AS revisionindicator
FROM "ny-fed-reference-rates-secured"
