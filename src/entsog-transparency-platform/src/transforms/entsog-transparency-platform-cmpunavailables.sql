WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-cmpunavailables"
)
SELECT
    id,
    operatorKey                             AS operator_key,
    operatorLabel                           AS operator_label,
    pointKey                                AS point_key,
    pointLabel                              AS point_label,
    directionKey                            AS direction_key,
    allocationProcess                       AS allocation_process,
    TRY_CAST(periodFrom AS TIMESTAMP)       AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)         AS period_to,
    NULLIF(generalRemarks, '')              AS general_remarks,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP) AS last_update
FROM ranked
WHERE rn = 1
