SELECT
    strptime(delivery_date, '%Y/%m/%d')::DATE AS date,
    CAST(slot AS INTEGER)                     AS slot,
    CAST(system_price AS DOUBLE)              AS system_price,
    CAST(area_price_hokkaido AS DOUBLE)       AS area_price_hokkaido,
    CAST(area_price_tohoku   AS DOUBLE)       AS area_price_tohoku,
    CAST(area_price_tokyo    AS DOUBLE)       AS area_price_tokyo,
    CAST(area_price_chubu    AS DOUBLE)       AS area_price_chubu,
    CAST(area_price_hokuriku AS DOUBLE)       AS area_price_hokuriku,
    CAST(area_price_kansai   AS DOUBLE)       AS area_price_kansai,
    CAST(area_price_chugoku  AS DOUBLE)       AS area_price_chugoku,
    CAST(area_price_shikoku  AS DOUBLE)       AS area_price_shikoku,
    CAST(area_price_kyushu   AS DOUBLE)       AS area_price_kyushu,
    CAST(sell_bid_volume_kwh AS DOUBLE)       AS sell_bid_volume_kwh,
    CAST(buy_bid_volume_kwh  AS DOUBLE)       AS buy_bid_volume_kwh,
    CAST(contract_volume_kwh AS DOUBLE)       AS contract_volume_kwh
FROM "jepx-spot-market"
WHERE delivery_date IS NOT NULL
  AND slot BETWEEN 1 AND 48
QUALIFY row_number() OVER (PARTITION BY date, slot ORDER BY date) = 1
