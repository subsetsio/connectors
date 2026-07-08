SELECT
    range,
    ROW_NUMBER() OVER (PARTITION BY range ORDER BY listen_count DESC, release_name) AS rank,
    release_mbid,
    release_name,
    artist_name,
    array_to_string(artist_mbids, ',') AS artist_mbids,
    CAST(caa_id AS BIGINT) AS caa_id,
    caa_release_mbid,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(window_from_ts) AS TIMESTAMP) AS window_start, CAST(to_timestamp(window_to_ts)   AS TIMESTAMP) AS window_end, CAST(to_timestamp(last_updated)   AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-releases"
WHERE release_name IS NOT NULL AND listen_count IS NOT NULL
