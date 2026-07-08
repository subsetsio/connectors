SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-6c5e4b9a-97bd-4ea7-96eb-a077bbf57692"
WHERE value IS NOT NULL AND value <> ''
