-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "issuingorganization",
    "feedname",
    "url",
    "format",
    CAST("active" AS BOOLEAN) AS active,
    "datafeed_frequency_update",
    "version",
    CAST("sdate" AS TIMESTAMP) AS sdate,
    CAST("edate" AS TIMESTAMP) AS edate,
    CAST("needapikey" AS BOOLEAN) AS needapikey,
    "apikeyurl",
    "geocoded_column"
FROM "u-s-department-of-transportation-69qe-yiui"
