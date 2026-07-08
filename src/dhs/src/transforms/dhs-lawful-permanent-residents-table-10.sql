SELECT
    topic,
    table_label,
    title,
    section,
    category,
    breakdown,
    CAST(value AS DOUBLE) AS value,
    value_note
FROM "dhs-lawful-permanent-residents-table-10"
WHERE category IS NOT NULL AND category <> ''
