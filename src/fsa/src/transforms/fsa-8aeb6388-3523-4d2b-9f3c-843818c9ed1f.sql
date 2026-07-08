SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-8aeb6388-3523-4d2b-9f3c-843818c9ed1f"
WHERE value IS NOT NULL AND value <> ''
