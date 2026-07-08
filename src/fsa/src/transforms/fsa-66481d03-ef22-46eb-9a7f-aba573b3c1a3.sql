SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-66481d03-ef22-46eb-9a7f-aba573b3c1a3"
WHERE value IS NOT NULL AND value <> ''
