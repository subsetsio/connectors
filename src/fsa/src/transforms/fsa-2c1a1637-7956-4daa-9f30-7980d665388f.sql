SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-2c1a1637-7956-4daa-9f30-7980d665388f"
WHERE value IS NOT NULL AND value <> ''
