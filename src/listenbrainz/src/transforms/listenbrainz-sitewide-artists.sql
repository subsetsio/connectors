SELECT
    range,
    ROW_NUMBER() OVER (PARTITION BY range ORDER BY listen_count DESC, artist_name) AS rank,
    artist_mbid,
    artist_name,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(window_from_ts) AS TIMESTAMP) AS window_start, CAST(to_timestamp(window_to_ts)   AS TIMESTAMP) AS window_end, CAST(to_timestamp(last_updated)   AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-artists"
WHERE artist_name IS NOT NULL AND listen_count IS NOT NULL
