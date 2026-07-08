SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-e94f4c4c-c753-4bc0-b106-30feb28fbf66"
WHERE value IS NOT NULL AND value <> ''
