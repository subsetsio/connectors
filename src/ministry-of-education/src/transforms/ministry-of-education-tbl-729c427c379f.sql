SELECT DISTINCT
    CAST(year AS INTEGER)    AS year,
    CAST(tbl_idx AS INTEGER) AS table_index,
    CAST(row_idx AS INTEGER) AS row_index,
    CAST(col_idx AS INTEGER) AS col_index,
    row_label,
    col_label,
    CAST(value AS DOUBLE)    AS value
FROM "ministry-of-education-tbl-729c427c379f"
WHERE value IS NOT NULL AND row_label IS NOT NULL AND row_label <> ''
