SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-e1214317-0f0f-4772-91d6-f95e178c4c30"
WHERE value IS NOT NULL AND value <> ''
