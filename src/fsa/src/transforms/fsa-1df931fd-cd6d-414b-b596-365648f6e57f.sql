SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-1df931fd-cd6d-414b-b596-365648f6e57f"
WHERE value IS NOT NULL AND value <> ''
