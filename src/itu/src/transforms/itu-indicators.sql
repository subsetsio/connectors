SELECT
    code_id,
    code,
    label,
    category,
    sub_category,
    answer_type,
    start_year,
    database_id,
    collection_indicator,
    disaggregation,
    code_desc
FROM "itu-indicators"
WHERE code_id IS NOT NULL
