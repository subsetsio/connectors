SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-f329cf12-c12f-4d73-94c5-68222c7601aa"
WHERE value IS NOT NULL AND value <> ''
