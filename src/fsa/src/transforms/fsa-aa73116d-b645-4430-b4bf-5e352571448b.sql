SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-aa73116d-b645-4430-b4bf-5e352571448b"
WHERE value IS NOT NULL AND value <> ''
