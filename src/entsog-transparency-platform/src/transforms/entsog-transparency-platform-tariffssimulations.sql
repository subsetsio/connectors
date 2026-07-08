WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-tariffssimulations"
)
SELECT
    id,
    operatorKey                                                AS operator_key,
    operator                                                   AS operator_label,
    pointKey                                                   AS point_key,
    pointLabel                                                 AS point_label,
    directionKey                                               AS direction_key,
    countryCode                                                AS country_code,
    fromBZ                                                     AS from_bz,
    toBZ                                                       AS to_bz,
    productType                                                AS product_type,
    tariffCapacityType                                         AS tariff_capacity_type,
    operatorCurrency                                           AS operator_currency,
    TRY_CAST(NULLIF(productSimulationCostInLocalCurrency, '') AS DOUBLE) AS cost_local,
    TRY_CAST(NULLIF(productSimulationCostInEURO, '') AS DOUBLE)          AS cost_eur,
    TRY_CAST(periodFrom AS TIMESTAMP)                          AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)                            AS period_to,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)                  AS last_update
FROM ranked
WHERE rn = 1
