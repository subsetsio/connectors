SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d9eedca9-da25-4f91-92f5-631ba1894b83"
WHERE value IS NOT NULL AND value <> ''
