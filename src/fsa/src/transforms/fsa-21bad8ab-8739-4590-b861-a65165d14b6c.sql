SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-21bad8ab-8739-4590-b861-a65165d14b6c"
WHERE value IS NOT NULL AND value <> ''
