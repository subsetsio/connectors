SELECT
    CAST("id" AS BIGINT)        AS id,
    CAST("tradeId" AS BIGINT)   AS trade_id,
    "buyer"                     AS buyer,
    "seller"                    AS seller,
    "category"                  AS category,
    "subCategory"               AS sub_category,
    "desg"                      AS weapon_designation,
    "desc"                      AS weapon_description,
    CAST("orderYr" AS INTEGER)  AS order_year,
    CAST("deliveryYr" AS INTEGER) AS delivery_year,
    CAST("units" AS DOUBLE)     AS units,
    "status"                    AS status,
    "transferType"              AS transfer_type,
    CAST("orderYrEst" AS BOOLEAN)  AS order_year_estimated,
    CAST("unitsEst" AS BOOLEAN)    AS units_estimated,
    CAST("statusEst" AS BOOLEAN)   AS status_estimated
FROM "sipri-arms-transfers"
WHERE "id" IS NOT NULL
