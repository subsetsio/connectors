SELECT
    commodity,
    variety,
    market,
    original_measure,
    standard_measure,
    original_currency,
    standard_currency,
    CAST(item_year AS INTEGER)        AS year,
    item_value_original               AS value_original,
    item_value_standardized           AS value_standardized,
    notes,
    source_raw                        AS source
FROM "allen-unger-commodity-prices-commodities"
WHERE item_year IS NOT NULL
  AND commodity IS NOT NULL
  AND market IS NOT NULL
