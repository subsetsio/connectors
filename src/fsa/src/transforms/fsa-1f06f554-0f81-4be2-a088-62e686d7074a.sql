SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-1f06f554-0f81-4be2-a088-62e686d7074a"
WHERE value IS NOT NULL AND value <> ''
