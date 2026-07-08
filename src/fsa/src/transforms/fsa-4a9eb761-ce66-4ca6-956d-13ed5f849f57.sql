SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4a9eb761-ce66-4ca6-956d-13ed5f849f57"
WHERE value IS NOT NULL AND value <> ''
