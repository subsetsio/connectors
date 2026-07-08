WITH norm AS (
    SELECT
        CAST(strptime(period || '01', '%Y%m%d') AS DATE) AS month,
        NULLIF(TRIM(country), '') AS country,
        NULLIF(TRIM(region), '')  AS region,
        NULLIF(TRIM(crop), '')    AS crop,
        CASE
            WHEN UPPER(TRIM(conditions)) IN ('', 'NO DATA', '#N/A', 'N/A', 'NA')
                THEN NULL
            -- unambiguous source spelling errors of 'Favourable'
            WHEN TRIM(conditions) IN ('Favuorable', 'Favourble')
                THEN 'Favourable'
            ELSE TRIM(conditions)
        END AS condition,
        CASE
            WHEN UPPER(TRIM(drivers)) IN ('', 'NO DATA', '#N/A', 'N/A', 'NA')
            THEN NULL ELSE TRIM(drivers)
        END AS drivers
    FROM "geoglam-crop-monitor-crop-conditions"
),
ranked AS (
    SELECT *,
        row_number() OVER (
            PARTITION BY month, country, region, crop
            ORDER BY CASE WHEN condition IS NULL THEN 1 ELSE 0 END
        ) AS rn
    FROM norm
    WHERE country IS NOT NULL
      AND region IS NOT NULL
      AND crop IS NOT NULL
      AND month IS NOT NULL
)
SELECT month, country, region, crop, condition, drivers
FROM ranked
WHERE rn = 1
