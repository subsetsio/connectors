SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c3fe9b01-f80a-41cd-94d1-a86327814e01"
WHERE value IS NOT NULL AND value <> ''
