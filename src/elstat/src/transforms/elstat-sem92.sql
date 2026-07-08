SELECT
    source_file,
    sheet,
    row_label,
    col_label,
    CAST(row_idx AS BIGINT) AS row_idx,
    CAST(col_idx AS BIGINT) AS col_idx,
    CAST(value AS DOUBLE)   AS value
FROM "elstat-sem92"
WHERE value IS NOT NULL
