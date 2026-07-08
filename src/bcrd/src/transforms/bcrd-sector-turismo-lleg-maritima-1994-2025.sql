SELECT
    file,
    sheet,
    CAST("row" AS INTEGER) AS row_idx,
    CAST("col" AS INTEGER) AS col_idx,
    row_label,
    value         AS value_text,
    CAST(num AS DOUBLE) AS value_num
FROM "bcrd-sector-turismo-lleg-maritima-1994-2025"
WHERE value IS NOT NULL
