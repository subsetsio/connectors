SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c0c0d8e2-7315-4f98-9924-c4e8887d1159"
WHERE value IS NOT NULL AND value <> ''
