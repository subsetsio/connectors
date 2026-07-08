SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-0de65bee-630e-4ea7-91dc-ccade64a1b1b"
WHERE value IS NOT NULL AND value <> ''
