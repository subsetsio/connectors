SELECT
    range,
    country,
    CAST(artist_count AS BIGINT) AS artist_count,
    CAST(listen_count AS BIGINT) AS listen_count,
    CAST(to_timestamp(last_updated) AS TIMESTAMP) AS updated_at
FROM "listenbrainz-sitewide-artist-map"
WHERE country IS NOT NULL
