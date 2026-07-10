SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-f454d151-d736-48b1-9287-3359740cab99"
WHERE value IS NOT NULL AND value <> ''
