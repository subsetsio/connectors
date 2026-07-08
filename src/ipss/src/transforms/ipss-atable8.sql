SELECT
    CAST(sheet AS VARCHAR)     AS sheet,
    CAST(row AS INTEGER)       AS row,
    CAST(col AS INTEGER)       AS col,
    CAST(row_label AS VARCHAR) AS row_label,
    CAST(col_label AS VARCHAR) AS col_label,
    CAST(value AS DOUBLE)      AS value
FROM "ipss-atable8"
WHERE value IS NOT NULL
