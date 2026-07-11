SELECT
    CAST(sheet AS VARCHAR)       AS sheet,
    CAST(excel_row AS INTEGER)   AS excel_row,
    CAST(excel_col AS INTEGER)   AS excel_col,
    CAST(row_label AS VARCHAR)   AS row_label,
    CAST(col_label AS VARCHAR)   AS col_label,
    CAST(value_num AS DOUBLE)    AS value_num,
    CAST(value_text AS VARCHAR)  AS value_text
FROM "obr-long-term-economic-determinants-economic-and-fiscal-outlook"
WHERE value_num IS NOT NULL OR value_text IS NOT NULL
