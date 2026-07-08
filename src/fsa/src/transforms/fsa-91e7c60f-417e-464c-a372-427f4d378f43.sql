SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-91e7c60f-417e-464c-a372-427f4d378f43"
WHERE value IS NOT NULL AND value <> ''
