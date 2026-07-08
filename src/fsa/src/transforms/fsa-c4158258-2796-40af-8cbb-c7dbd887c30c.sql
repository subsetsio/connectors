SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c4158258-2796-40af-8cbb-c7dbd887c30c"
WHERE value IS NOT NULL AND value <> ''
