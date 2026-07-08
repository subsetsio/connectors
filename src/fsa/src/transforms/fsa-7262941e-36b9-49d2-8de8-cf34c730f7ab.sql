SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-7262941e-36b9-49d2-8de8-cf34c730f7ab"
WHERE value IS NOT NULL AND value <> ''
