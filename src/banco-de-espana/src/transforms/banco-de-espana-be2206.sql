SELECT series_code, alias, description, units, frequency, period_label, CAST(date AS DATE) AS date, CAST(value AS DOUBLE) AS value FROM "banco-de-espana-be2206" WHERE value IS NOT NULL
