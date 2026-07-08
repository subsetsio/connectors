SELECT
    CAST(strptime(month || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS date,
    country,
    CAST(events AS BIGINT) AS events
FROM "acled-demonstration-events"
WHERE month IS NOT NULL AND year IS NOT NULL
