SELECT
    symbol,
    strptime(date, '%m/%d/%Y')::DATE AS date,
    open,
    high,
    low,
    close
FROM "cboe-global-markets-values"
WHERE date IS NOT NULL
  AND close IS NOT NULL
