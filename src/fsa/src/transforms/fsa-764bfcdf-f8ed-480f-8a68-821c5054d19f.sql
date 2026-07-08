SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-764bfcdf-f8ed-480f-8a68-821c5054d19f"
WHERE value IS NOT NULL AND value <> ''
