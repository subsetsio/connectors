SELECT
    CAST(date AS DATE)                  AS date,
    seasonal_adjustment,
    CAST(ivey_pmi AS DOUBLE)            AS ivey_pmi,
    CAST(employment_index AS DOUBLE)    AS employment_index,
    CAST(inventories_index AS DOUBLE)   AS inventories_index,
    CAST(deliveries_index AS DOUBLE)    AS deliveries_index,
    CAST(prices_index AS DOUBLE)        AS prices_index
FROM "ivey-purchasing-managers-index-ivey-pmi"
WHERE date IS NOT NULL
  AND ivey_pmi IS NOT NULL
