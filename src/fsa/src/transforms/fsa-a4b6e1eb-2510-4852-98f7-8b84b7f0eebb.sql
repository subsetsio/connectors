SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-a4b6e1eb-2510-4852-98f7-8b84b7f0eebb"
WHERE value IS NOT NULL AND value <> ''
