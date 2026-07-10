SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d8d3ae4f-b99d-4885-a4d3-6a5b77d66ca8"
WHERE value IS NOT NULL AND value <> ''
