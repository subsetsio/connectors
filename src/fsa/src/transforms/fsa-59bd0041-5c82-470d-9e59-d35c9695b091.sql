SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-59bd0041-5c82-470d-9e59-d35c9695b091"
WHERE value IS NOT NULL AND value <> ''
