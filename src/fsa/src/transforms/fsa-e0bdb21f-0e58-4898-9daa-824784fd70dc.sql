SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-e0bdb21f-0e58-4898-9daa-824784fd70dc"
WHERE value IS NOT NULL AND value <> ''
