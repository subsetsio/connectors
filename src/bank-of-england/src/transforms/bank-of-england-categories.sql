SELECT
    CAST(category_id AS VARCHAR)    AS category_id,
    CAST(category_name AS VARCHAR)  AS category_name,
    CAST(meaning_id AS VARCHAR)     AS meaning_id,
    CAST(category_value AS VARCHAR) AS category_value
FROM "bank-of-england-categories"
WHERE category_id IS NOT NULL
  AND meaning_id IS NOT NULL
