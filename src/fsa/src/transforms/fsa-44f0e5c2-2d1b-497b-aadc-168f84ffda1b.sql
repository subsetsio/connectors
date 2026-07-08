SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-44f0e5c2-2d1b-497b-aadc-168f84ffda1b"
WHERE value IS NOT NULL AND value <> ''
