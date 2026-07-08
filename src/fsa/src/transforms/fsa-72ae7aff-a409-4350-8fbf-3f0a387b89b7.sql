SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-72ae7aff-a409-4350-8fbf-3f0a387b89b7"
WHERE value IS NOT NULL AND value <> ''
