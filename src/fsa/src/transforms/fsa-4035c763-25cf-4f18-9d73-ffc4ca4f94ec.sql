SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4035c763-25cf-4f18-9d73-ffc4ca4f94ec"
WHERE value IS NOT NULL AND value <> ''
