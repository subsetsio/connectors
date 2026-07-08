SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d42b5698-d45c-4c85-8ab9-4d0bc0d96154"
WHERE value IS NOT NULL AND value <> ''
