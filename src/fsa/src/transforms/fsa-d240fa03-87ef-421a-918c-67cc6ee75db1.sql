SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d240fa03-87ef-421a-918c-67cc6ee75db1"
WHERE value IS NOT NULL AND value <> ''
