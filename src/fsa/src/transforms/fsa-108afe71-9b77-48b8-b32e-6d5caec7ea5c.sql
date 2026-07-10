SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-108afe71-9b77-48b8-b32e-6d5caec7ea5c"
WHERE value IS NOT NULL AND value <> ''
