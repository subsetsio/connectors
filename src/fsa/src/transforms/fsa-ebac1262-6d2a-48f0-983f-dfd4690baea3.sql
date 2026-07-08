SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-ebac1262-6d2a-48f0-983f-dfd4690baea3"
WHERE value IS NOT NULL AND value <> ''
