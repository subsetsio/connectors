-- fda-tobacco-problem: Tobacco product problem reports (Safety Reporting Portal). date_submitted arrives MM/DD/YYYY and is normalized to ISO by the fetch.
SELECT
    TRY_CAST(TRY_CAST("report_id" AS DOUBLE) AS BIGINT) AS report_id,
    TRY_CAST("date_submitted" AS DATE) AS date_submitted,
    "nonuser_affected" AS nonuser_affected,
    TRY_CAST(TRY_CAST("number_tobacco_products" AS DOUBLE) AS BIGINT) AS number_tobacco_products,
    TRY_CAST(TRY_CAST("number_health_problems" AS DOUBLE) AS BIGINT) AS number_health_problems,
    TRY_CAST(TRY_CAST("number_product_problems" AS DOUBLE) AS BIGINT) AS number_product_problems
FROM "fda-tobacco-problem"
