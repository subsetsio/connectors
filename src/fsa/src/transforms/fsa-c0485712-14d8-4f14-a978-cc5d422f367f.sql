SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-c0485712-14d8-4f14-a978-cc5d422f367f"
WHERE value IS NOT NULL AND value <> ''
