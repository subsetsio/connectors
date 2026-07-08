SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-26f5ce30-73bd-4835-b234-99da3b11b299"
WHERE value IS NOT NULL AND value <> ''
