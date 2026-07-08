SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-219eef3b-b7db-473f-937f-42a290380cc7"
WHERE value IS NOT NULL AND value <> ''
