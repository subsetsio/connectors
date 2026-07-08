SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-0d0a5b2a-a23e-4bce-a13c-2f6b0ce8a69e"
WHERE value IS NOT NULL AND value <> ''
