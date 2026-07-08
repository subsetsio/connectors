SELECT
    resource_id,
    resource_name,
    sheet,
    CAST(row_idx AS INTEGER) AS row_idx,
    CAST(col_idx AS INTEGER) AS col_idx,
    value,
    num_value
FROM "fsa-58724edc-0b85-4f91-a200-17d6fb461cfb"
WHERE value IS NOT NULL AND value <> ''
