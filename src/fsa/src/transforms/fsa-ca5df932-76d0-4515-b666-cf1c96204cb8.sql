SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-ca5df932-76d0-4515-b666-cf1c96204cb8"
WHERE value IS NOT NULL AND value <> ''
