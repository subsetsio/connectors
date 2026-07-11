SELECT
  CAST(MonthId AS INTEGER) AS month_id,
  make_date(CAST(FLOOR(MonthId / 100) AS INTEGER), CAST(MonthId % 100 AS INTEGER), 1) AS month,
  CAST(Year AS INTEGER) AS year,
  CAST(MonthNumeric AS INTEGER) AS month_numeric,
  CAST(QuarterNumeric AS INTEGER) AS quarter_numeric,
  CAST(MonthName AS VARCHAR) AS month_name
FROM "hmrc-date"
