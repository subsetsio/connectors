SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4681aa2c-8835-412b-ab29-485d9f8f59dc"
WHERE value IS NOT NULL AND value <> ''
