SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-a0df1c82-f72d-4232-bfd6-94d2bbae4968"
WHERE value IS NOT NULL AND value <> ''
