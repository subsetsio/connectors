SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-d45a075a-ce12-4be9-a339-6f4f8dffc775"
WHERE value IS NOT NULL AND value <> ''
