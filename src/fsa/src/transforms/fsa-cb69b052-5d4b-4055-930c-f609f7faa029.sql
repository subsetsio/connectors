SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-cb69b052-5d4b-4055-930c-f609f7faa029"
WHERE value IS NOT NULL AND value <> ''
