SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-21f52561-926d-4d2a-8fe7-6166cb1a74ce"
WHERE value IS NOT NULL AND value <> ''
