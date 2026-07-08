SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-bdec1cf0-cfb0-4297-be58-16642f6b5179"
WHERE value IS NOT NULL AND value <> ''
