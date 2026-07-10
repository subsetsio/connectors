SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-dbdc6b34-a9d9-4c6e-bcd6-043efb6c3fd1"
WHERE value IS NOT NULL AND value <> ''
