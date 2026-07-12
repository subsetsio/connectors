SELECT
    range,
    CAST(year AS INTEGER) AS year,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(last_updated) AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-era-activity"
WHERE year IS NOT NULL AND listen_count IS NOT NULL
