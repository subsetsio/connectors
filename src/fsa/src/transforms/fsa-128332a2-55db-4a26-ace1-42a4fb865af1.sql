SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-128332a2-55db-4a26-ace1-42a4fb865af1"
WHERE value IS NOT NULL AND value <> ''
