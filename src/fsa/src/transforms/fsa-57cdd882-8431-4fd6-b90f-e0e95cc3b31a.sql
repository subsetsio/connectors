SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-57cdd882-8431-4fd6-b90f-e0e95cc3b31a"
WHERE value IS NOT NULL AND value <> ''
