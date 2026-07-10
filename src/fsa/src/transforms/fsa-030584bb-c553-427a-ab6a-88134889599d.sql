SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-030584bb-c553-427a-ab6a-88134889599d"
WHERE value IS NOT NULL AND value <> ''
