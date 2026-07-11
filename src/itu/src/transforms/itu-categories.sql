SELECT
    category,
    category_sort,
    sub_category,
    sub_category_sort,
    code_id,
    label,
    database_id,
    series_type,
    indicator_sort,
    external,
    is_collection
FROM "itu-categories"
WHERE category IS NOT NULL
  AND sub_category IS NOT NULL
  AND code_id IS NOT NULL
