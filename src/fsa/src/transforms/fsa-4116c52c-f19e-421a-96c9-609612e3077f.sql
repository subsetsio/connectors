SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4116c52c-f19e-421a-96c9-609612e3077f"
WHERE value IS NOT NULL AND value <> ''
