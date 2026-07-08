SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d8aee855-092d-410a-96f7-ce45b0b56041"
WHERE value IS NOT NULL AND value <> ''
