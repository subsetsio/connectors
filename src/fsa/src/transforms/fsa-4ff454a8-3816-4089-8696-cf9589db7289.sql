SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4ff454a8-3816-4089-8696-cf9589db7289"
WHERE value IS NOT NULL AND value <> ''
