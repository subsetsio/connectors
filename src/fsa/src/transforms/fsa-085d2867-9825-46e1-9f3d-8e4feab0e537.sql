SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-085d2867-9825-46e1-9f3d-8e4feab0e537"
WHERE value IS NOT NULL AND value <> ''
