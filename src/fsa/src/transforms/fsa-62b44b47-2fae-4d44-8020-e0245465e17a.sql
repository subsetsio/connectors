SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-62b44b47-2fae-4d44-8020-e0245465e17a"
WHERE value IS NOT NULL AND value <> ''
