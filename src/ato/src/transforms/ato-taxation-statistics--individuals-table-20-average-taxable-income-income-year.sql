SELECT
  CAST(postcode AS VARCHAR) AS postcode,
  TRY_CAST(REPLACE(average_taxable_income, ',', '') AS BIGINT) AS average_taxable_income,
  CAST(income_year AS VARCHAR) AS income_year
FROM "ato-taxation-statistics--individuals-table-20-average-taxable-income-income-year"
