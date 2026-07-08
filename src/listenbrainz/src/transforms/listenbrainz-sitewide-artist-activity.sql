SELECT
    range,
    name AS artist_name,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(window_from_ts) AS TIMESTAMP) AS window_start, CAST(to_timestamp(window_to_ts)   AS TIMESTAMP) AS window_end, CAST(to_timestamp(last_updated)   AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-artist-activity"
WHERE name IS NOT NULL AND listen_count IS NOT NULL
