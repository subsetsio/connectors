SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d87c57bd-a422-4a57-a6ed-d5e11f837203"
WHERE value IS NOT NULL AND value <> ''
