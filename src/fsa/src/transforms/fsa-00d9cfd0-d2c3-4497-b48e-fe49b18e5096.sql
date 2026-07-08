SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-00d9cfd0-d2c3-4497-b48e-fe49b18e5096"
WHERE value IS NOT NULL AND value <> ''
