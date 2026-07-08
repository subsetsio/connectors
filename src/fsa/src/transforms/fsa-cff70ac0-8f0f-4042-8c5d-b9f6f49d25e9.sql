SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-cff70ac0-8f0f-4042-8c5d-b9f6f49d25e9"
WHERE value IS NOT NULL AND value <> ''
