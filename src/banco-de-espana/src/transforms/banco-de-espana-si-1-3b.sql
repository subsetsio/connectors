SELECT series_code, alias, description, units, frequency, period_label, CAST(date AS DATE) AS date, CAST(value AS DOUBLE) AS value FROM "banco-de-espana-si-1-3b" WHERE value IS NOT NULL
