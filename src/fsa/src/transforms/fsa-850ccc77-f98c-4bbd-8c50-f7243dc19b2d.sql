SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-850ccc77-f98c-4bbd-8c50-f7243dc19b2d"
WHERE value IS NOT NULL AND value <> ''
