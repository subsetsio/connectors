SELECT
    topic,
    table_label,
    title,
    section,
    category,
    breakdown,
    CAST(value AS DOUBLE) AS value,
    value_note
FROM "dhs-naturalizations-table-25"
WHERE category IS NOT NULL AND category <> ''
