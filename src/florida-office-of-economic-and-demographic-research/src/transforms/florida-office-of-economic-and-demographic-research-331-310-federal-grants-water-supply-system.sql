SELECT
    sheet,
    row_dim,
    row_label,
    measure,
    CAST(value_num AS DOUBLE) AS value,
    value_text
FROM "florida-office-of-economic-and-demographic-research-331-310-federal-grants-water-supply-system"
WHERE value_text IS NOT NULL
