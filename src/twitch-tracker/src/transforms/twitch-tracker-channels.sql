SELECT
    channel,
    CAST(rank AS INTEGER)             AS rank,
    CAST(minutes_streamed AS BIGINT)  AS minutes_streamed,
    CAST(avg_viewers AS BIGINT)       AS avg_viewers,
    CAST(max_viewers AS BIGINT)       AS max_viewers,
    CAST(hours_watched AS BIGINT)     AS hours_watched,
    CAST(followers AS BIGINT)         AS followers,
    CAST(followers_total AS BIGINT)   AS followers_total,
    CAST(captured_date AS DATE)       AS captured_date
FROM "twitch-tracker-channels"
WHERE channel IS NOT NULL
