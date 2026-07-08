SELECT
    game,
    CAST(rank AS INTEGER)         AS rank,
    CAST(avg_viewers AS BIGINT)   AS avg_viewers,
    CAST(avg_channels AS BIGINT)  AS avg_channels,
    CAST(hours_watched AS BIGINT) AS hours_watched,
    CAST(captured_date AS DATE)   AS captured_date
FROM "twitch-tracker-games"
WHERE game IS NOT NULL
