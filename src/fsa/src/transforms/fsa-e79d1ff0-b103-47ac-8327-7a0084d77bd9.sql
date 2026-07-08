SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-e79d1ff0-b103-47ac-8327-7a0084d77bd9"
WHERE value IS NOT NULL AND value <> ''
