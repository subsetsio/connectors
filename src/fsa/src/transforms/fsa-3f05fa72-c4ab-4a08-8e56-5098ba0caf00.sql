SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-3f05fa72-c4ab-4a08-8e56-5098ba0caf00"
WHERE value IS NOT NULL AND value <> ''
