SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-93236a31-062d-46bf-b9a4-f72acdf5edbb"
WHERE value IS NOT NULL AND value <> ''
