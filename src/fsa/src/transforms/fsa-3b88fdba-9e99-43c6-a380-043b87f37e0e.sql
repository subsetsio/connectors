SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-3b88fdba-9e99-43c6-a380-043b87f37e0e"
WHERE value IS NOT NULL AND value <> ''
