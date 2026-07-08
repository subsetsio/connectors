SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-db8f453f-2f09-4fd6-a2ac-11f1c944cb5d"
WHERE value IS NOT NULL AND value <> ''
