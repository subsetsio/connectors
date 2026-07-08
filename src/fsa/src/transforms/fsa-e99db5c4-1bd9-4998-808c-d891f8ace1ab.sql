SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-e99db5c4-1bd9-4998-808c-d891f8ace1ab"
WHERE value IS NOT NULL AND value <> ''
