SELECT CAST(date AS DATE) AS date, series_name, category, subcategory,
       CAST(value AS DOUBLE) AS value
FROM "bruegel-divisia-monetary-aggregates-euro-area" WHERE value IS NOT NULL
