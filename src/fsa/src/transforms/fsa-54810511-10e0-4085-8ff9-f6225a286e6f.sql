SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-54810511-10e0-4085-8ff9-f6225a286e6f"
WHERE value IS NOT NULL AND value <> ''
