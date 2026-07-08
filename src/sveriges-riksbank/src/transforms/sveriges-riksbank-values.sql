SELECT series_id, group_id, date, value
FROM (
    SELECT
        series_id,
        group_id,
        CAST(date AS DATE)   AS date,
        CAST(value AS DOUBLE) AS value,
        row_number() OVER (
            PARTITION BY series_id, CAST(date AS DATE)
            ORDER BY value
        ) AS rn
    FROM "sveriges-riksbank-values"
    WHERE series_id IS NOT NULL
      AND date IS NOT NULL
      AND value IS NOT NULL
)
WHERE rn = 1
