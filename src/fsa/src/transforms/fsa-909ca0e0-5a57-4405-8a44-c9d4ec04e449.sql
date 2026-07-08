SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-909ca0e0-5a57-4405-8a44-c9d4ec04e449"
WHERE value IS NOT NULL AND value <> ''
