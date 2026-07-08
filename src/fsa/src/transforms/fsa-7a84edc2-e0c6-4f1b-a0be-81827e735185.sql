SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-7a84edc2-e0c6-4f1b-a0be-81827e735185"
WHERE value IS NOT NULL AND value <> ''
