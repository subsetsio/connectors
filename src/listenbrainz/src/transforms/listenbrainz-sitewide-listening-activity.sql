SELECT
    range,
    time_range,
    CAST(to_timestamp(from_ts) AS TIMESTAMP) AS bucket_start,
    CAST(to_timestamp(to_ts)   AS TIMESTAMP) AS bucket_end,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(last_updated) AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-listening-activity"
WHERE time_range IS NOT NULL AND listen_count IS NOT NULL
