SELECT
    series_id,
    CAST(year AS INTEGER)                            AS year,
    period,
    CAST(substr(period, 2, 2) AS INTEGER)            AS month,
    make_date(CAST(year AS INTEGER),
              CAST(substr(period, 2, 2) AS INTEGER), 1) AS month_start,
    CAST(value AS DOUBLE)                            AS value
FROM "american-staffing-association-bls-monthly-employment"
WHERE series_id IS NOT NULL
  AND year IS NOT NULL
  AND period IS NOT NULL
  AND value IS NOT NULL
