SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c973159d-9132-41dc-88f8-d098cc27d96e"
WHERE value IS NOT NULL AND value <> ''
