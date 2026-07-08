SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d74d82b5-338f-4f0c-869e-c41e6a575c1d"
WHERE value IS NOT NULL AND value <> ''
