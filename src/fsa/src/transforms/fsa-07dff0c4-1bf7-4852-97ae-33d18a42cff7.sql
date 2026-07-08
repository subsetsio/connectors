SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-07dff0c4-1bf7-4852-97ae-33d18a42cff7"
WHERE value IS NOT NULL AND value <> ''
