-- The RBI home-page snapshot puts every headline number in one `rate` column
-- regardless of unit. Keep the percent-per-annum monetary rates and drop the
-- two rows that are not rates at all: "Exchange Rate" (a price level in INR
-- per USD) and "CPI Inflation" (a statistic). Excluding by name rather than
-- selecting by name so a rate the RBI adds later still lands here.
--
-- Residuals over the compiled pass-through:
--   * as_of_date is an ISO string in raw -> DATE
--   * currency_desc / time_month are null for every retained row -> dropped
--   * timedate_ms is the epoch-millis as_of_date was derived from -> dropped
--
-- caution: a current-value snapshot, overwritten each run — no rate history.
-- caution: WACR is a market-determined call-money rate the RBI targets, not
-- an instrument it sets.
SELECT
    CAST(name AS VARCHAR) AS rate_name,
    CAST(rate AS DOUBLE) AS rate_percent,
    strptime(as_of_date, '%Y-%m-%d')::DATE AS as_of_date
FROM "rbi-key-policy-rates"
WHERE name IS NOT NULL
  AND as_of_date IS NOT NULL
  AND rate IS NOT NULL
  AND name NOT ILIKE '%Exchange Rate%'
  AND name NOT ILIKE '%CPI%'
  AND name NOT ILIKE '%Inflation%'
