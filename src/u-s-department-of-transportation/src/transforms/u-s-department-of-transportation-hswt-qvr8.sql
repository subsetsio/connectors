-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reportyear" AS BIGINT) AS reportyear,
    "ntdid",
    "reportername",
    "modecd",
    "typeofservicecd",
    "primarysecuritytypedesc",
    CAST("primarysecuritytypecnt" AS DOUBLE) AS primarysecuritytypecnt,
    CAST("secondarypersonnelcnt" AS DOUBLE) AS secondarypersonnelcnt,
    CAST("totalpersonnelcnt" AS DOUBLE) AS totalpersonnelcnt,
    CAST("dedicatedtransitpolicefl" AS BOOLEAN) AS dedicatedtransitpolicefl,
    CAST("dedicatedlocalpolicefl" AS BOOLEAN) AS dedicatedlocalpolicefl,
    CAST("contractedlocallawenforc" AS BOOLEAN) AS contractedlocallawenforc,
    CAST("transitagencysecurityforcefl" AS BOOLEAN) AS transitagencysecurityforcefl,
    CAST("contractedsecurityforcefl" AS BOOLEAN) AS contractedsecurityforcefl,
    CAST("offdutypoliceofficersfl" AS BOOLEAN) AS offdutypoliceofficersfl,
    CAST("useoflocalpolicenoncontr" AS BOOLEAN) AS useoflocalpolicenoncontr
FROM "u-s-department-of-transportation-hswt-qvr8"
