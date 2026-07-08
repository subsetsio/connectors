WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-operatorpointdirections"
)
SELECT
    id,
    pointKey                            AS point_key,
    pointLabel                          AS point_label,
    operatorKey                         AS operator_key,
    operatorLabel                       AS operator_label,
    directionKey                        AS direction_key,
    TRY_CAST(tpTsoValidFrom AS TIMESTAMP) AS valid_from,
    TRY_CAST(tpTsoValidTo AS TIMESTAMP)   AS valid_to,
    tSOCountry                          AS tso_country,
    tSOBalancingZone                    AS tso_balancing_zone,
    crossBorderPointType               AS cross_border_point_type,
    pointType                           AS point_type,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP) AS last_update
FROM ranked
WHERE rn = 1
