SELECT DISTINCT
    CAST(park_id AS BIGINT)           AS park_id,
    park_name,
    CAST(year AS BIGINT)              AS year,
    CAST(annual_attendance AS BIGINT) AS annual_attendance
FROM "park-attendance-attendance"
-- Floor out implausibly tiny values: a commercial theme park's
-- annual attendance below 1,000 is not credible and indicates an
-- upstream typo (e.g. queue-times lists Chimelong Ocean Kingdom
-- 2013 as "11"). The lowest legitimate value observed is ~125,000.
WHERE annual_attendance >= 1000
  AND year BETWEEN 1950 AND 2100
