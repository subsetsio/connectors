WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-operationaldata"
)
SELECT
    id,
    indicator,
    periodType                                  AS period_type,
    TRY_CAST(periodFrom AS TIMESTAMP)           AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)             AS period_to,
    operatorKey                                 AS operator_key,
    operatorLabel                               AS operator_label,
    pointKey                                    AS point_key,
    pointLabel                                  AS point_label,
    directionKey                                AS direction_key,
    unit,
    TRY_CAST(NULLIF(value, '') AS DOUBLE)       AS value,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)   AS last_update
FROM ranked
WHERE rn = 1 AND TRY_CAST(NULLIF(value, '') AS DOUBLE) IS NOT NULL
