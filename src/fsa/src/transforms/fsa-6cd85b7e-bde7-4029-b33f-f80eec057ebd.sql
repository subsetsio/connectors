SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-6cd85b7e-bde7-4029-b33f-f80eec057ebd"
WHERE value IS NOT NULL AND value <> ''
