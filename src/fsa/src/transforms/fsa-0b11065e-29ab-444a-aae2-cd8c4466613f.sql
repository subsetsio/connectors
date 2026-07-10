SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-0b11065e-29ab-444a-aae2-cd8c4466613f"
WHERE value IS NOT NULL AND value <> ''
