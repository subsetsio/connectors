SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-4172787e-54a4-40ed-ba27-7c9426239ffc"
WHERE value IS NOT NULL AND value <> ''
