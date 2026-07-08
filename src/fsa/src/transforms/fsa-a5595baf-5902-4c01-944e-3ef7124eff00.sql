SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-a5595baf-5902-4c01-944e-3ef7124eff00"
WHERE value IS NOT NULL AND value <> ''
