SELECT
    CAST(series_code AS VARCHAR)    AS series_code,
    CAST(series_title AS VARCHAR)   AS series_title,
    CAST(category_id AS VARCHAR)    AS category_id,
    CAST(category_name AS VARCHAR)  AS category_name,
    CAST(meaning_id AS VARCHAR)     AS meaning_id,
    CAST(category_value AS VARCHAR) AS category_value
FROM "bank-of-england-series"
WHERE series_code IS NOT NULL
  AND category_id IS NOT NULL
  AND meaning_id IS NOT NULL
