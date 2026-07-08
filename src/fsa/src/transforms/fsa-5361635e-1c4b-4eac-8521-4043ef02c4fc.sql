SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-5361635e-1c4b-4eac-8521-4043ef02c4fc"
WHERE value IS NOT NULL AND value <> ''
