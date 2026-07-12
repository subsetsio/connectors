-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("notice_date" AS TIMESTAMP) AS notice_date,
    "job_site_name",
    "county_name",
    "wda_name",
    CAST("total_layoff_number" AS BIGINT) AS total_layoff_number,
    CAST("layoff_date" AS TIMESTAMP) AS layoff_date,
    CAST("wfdd_received_date" AS TIMESTAMP) AS wfdd_received_date,
    "city_name"
FROM "texas-workforce-commission-socrata-8w53-c4f6"
