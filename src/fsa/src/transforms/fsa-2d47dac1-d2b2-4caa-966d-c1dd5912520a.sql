SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-2d47dac1-d2b2-4caa-966d-c1dd5912520a"
WHERE value IS NOT NULL AND value <> ''
