SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-96e8a8cd-4c41-4ee5-bea5-66bbb67f5bc2"
WHERE value IS NOT NULL AND value <> ''
