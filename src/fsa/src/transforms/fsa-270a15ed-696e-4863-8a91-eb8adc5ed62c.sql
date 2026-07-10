SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-270a15ed-696e-4863-8a91-eb8adc5ed62c"
WHERE value IS NOT NULL AND value <> ''
