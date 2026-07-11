-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Missouri NVRA performance data is jurisdictional administration data; compare records within the same reporting period and jurisdiction type.
SELECT
    CAST("yrmo" AS DOUBLE) AS yrmo,
    CAST("month" AS DOUBLE) AS month,
    CAST("year" AS DOUBLE) AS year,
    "office",
    "county",
    "region",
    CAST("applications" AS BIGINT) AS applications,
    CAST("recertifications" AS BIGINT) AS recertifications,
    CAST("coaddress" AS BIGINT) AS coaddress,
    "vronly",
    CAST("totallog" AS BIGINT) AS totallog,
    CAST("yes" AS BIGINT) AS yes,
    CAST("no" AS BIGINT) AS no,
    CAST("noalreadyregistered" AS BIGINT) AS noalreadyregistered,
    CAST("blank" AS BIGINT) AS blank,
    CAST("totalcards" AS BIGINT) AS totalcards,
    CAST("post_settlement" AS BIGINT) AS post_settlement,
    CAST("months_after_settlement" AS BIGINT) AS months_after_settlement,
    "rate_yes",
    "rate_already",
    "rate_blank",
    "diff_totals",
    CAST("county_id" AS DOUBLE) AS county_id,
    "rate_yes2",
    CAST("multisite" AS BIGINT) AS multisite
FROM "mit-election-lab-dvn-ye2ee1"
