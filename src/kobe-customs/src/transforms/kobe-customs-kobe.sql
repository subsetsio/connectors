SELECT
    CAST(year AS INTEGER)        AS year,
    classification,
    sheet,
    row_label,
    col_header,
    CAST(row_idx AS INTEGER)     AS row_idx,
    CAST(col_idx AS INTEGER)     AS col_idx,
    CAST(value AS DOUBLE)        AS value
FROM "kobe-customs-kobe"
