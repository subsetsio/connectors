SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-fa7f8832-768e-4c21-81a2-e4c9306beaaf"
WHERE value IS NOT NULL AND value <> ''
