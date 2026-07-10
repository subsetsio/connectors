SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c6515677-c097-46d2-abd9-c105358516c1"
WHERE value IS NOT NULL AND value <> ''
