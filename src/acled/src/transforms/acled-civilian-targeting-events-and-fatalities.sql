SELECT
    CAST(strptime(month || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS date,
    country,
    CAST(events AS BIGINT) AS events,
    CAST(fatalities AS BIGINT) AS fatalities
FROM "acled-civilian-targeting-events-and-fatalities"
WHERE month IS NOT NULL AND year IS NOT NULL
