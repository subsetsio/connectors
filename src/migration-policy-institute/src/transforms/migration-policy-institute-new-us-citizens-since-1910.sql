SELECT
    sheet,
    CAST(row_id AS INTEGER)    AS row_id,
    CAST(col_index AS INTEGER) AS col_index,
    row_label,
    variable,
    value_text,
    value_num
FROM "migration-policy-institute-new-us-citizens-since-1910"
WHERE value_text IS NOT NULL
