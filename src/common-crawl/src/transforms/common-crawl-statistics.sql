SELECT
    crawl_id,
    CAST(crawl_date AS DATE)   AS crawl_date,
    metric_family,
    key,
    CAST("count" AS BIGINT)    AS count
FROM "common-crawl-statistics"
WHERE "count" IS NOT NULL
