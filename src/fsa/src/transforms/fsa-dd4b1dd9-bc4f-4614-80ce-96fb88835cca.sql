SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-dd4b1dd9-bc4f-4614-80ce-96fb88835cca"
WHERE value IS NOT NULL AND value <> ''
