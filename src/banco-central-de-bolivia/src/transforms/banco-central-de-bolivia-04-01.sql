SELECT
    table_code,
    sheet,
    CAST(row AS INTEGER) AS row,
    CAST(col AS INTEGER) AS col,
    value_num,
    value_text
FROM "banco-central-de-bolivia-04-01"
WHERE value_num IS NOT NULL OR value_text IS NOT NULL
