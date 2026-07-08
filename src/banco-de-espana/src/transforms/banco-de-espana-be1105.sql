SELECT series_code, alias, description, units, frequency, period_label, CAST(date AS DATE) AS date, CAST(value AS DOUBLE) AS value FROM "banco-de-espana-be1105" WHERE value IS NOT NULL
