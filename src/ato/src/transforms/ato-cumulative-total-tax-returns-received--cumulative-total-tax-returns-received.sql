SELECT
  CAST(income_year AS VARCHAR) AS income_year,
  COALESCE(
    CAST(TRY_STRPTIME(date, '%d/%m/%Y') AS DATE),
    TRY_CAST(date AS DATE)
  ) AS date,
  TRY_CAST(cumulative_total_tax_returns_received AS BIGINT) AS cumulative_total_tax_returns_received,
  TRY_CAST(electronic AS BIGINT) AS electronic,
  TRY_CAST(paper AS BIGINT) AS paper,
  TRY_CAST(of_current_year_returns_digitally_submitted AS DOUBLE) AS of_current_year_returns_digitally_submitted
FROM "ato-cumulative-total-tax-returns-received--cumulative-total-tax-returns-received"
WHERE date IS NOT NULL
