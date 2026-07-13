SELECT
    CAST(rank AS INTEGER)               AS rank,
    CAST(appid AS BIGINT)               AS appid,
    CAST(concurrent_in_game AS BIGINT)  AS concurrent_in_game,
    CAST(peak_in_game AS BIGINT)        AS peak_in_game,
    CAST(last_update AS TIMESTAMPTZ)    AS observed_at
FROM "steamdb-concurrent-players"
WHERE appid IS NOT NULL
ORDER BY rank
