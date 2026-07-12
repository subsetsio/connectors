SELECT
    geography,
    variety,
    market,
    name,
    CAST(year AS INTEGER) AS year,
    factor,
    unit,
    metal,
    source_location,
    source,
    notes,
    interpolated,
    constructed
FROM "allen-unger-commodity-prices-currencies"
WHERE year IS NOT NULL
  AND market IS NOT NULL
  AND name IS NOT NULL
