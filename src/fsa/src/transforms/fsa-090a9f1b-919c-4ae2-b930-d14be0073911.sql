SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-090a9f1b-919c-4ae2-b930-d14be0073911"
WHERE value IS NOT NULL AND value <> ''
