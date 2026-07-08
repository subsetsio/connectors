SELECT
    CAST(strptime(month || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS date,
    country, admin1, admin2, iso3, admin1_pcode, admin2_pcode,
    CAST(events AS BIGINT) AS events
FROM "acled-demonstration-events-subnational"
WHERE month IS NOT NULL AND year IS NOT NULL
  AND country IS NOT NULL AND admin1 IS NOT NULL AND admin2 IS NOT NULL
