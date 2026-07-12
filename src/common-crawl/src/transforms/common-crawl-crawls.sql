SELECT
    crawl_id,
    name,
    CAST(from_ts AS TIMESTAMP) AS from_ts,
    CAST(to_ts AS TIMESTAMP)   AS to_ts,
    cdx_api,
    timegate
FROM "common-crawl-crawls"
WHERE crawl_id IS NOT NULL
