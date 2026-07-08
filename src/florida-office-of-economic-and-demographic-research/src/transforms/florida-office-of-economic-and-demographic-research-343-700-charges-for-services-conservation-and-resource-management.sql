SELECT
    sheet,
    row_dim,
    row_label,
    measure,
    CAST(value_num AS DOUBLE) AS value,
    value_text
FROM "florida-office-of-economic-and-demographic-research-343-700-charges-for-services-conservation-and-resource-management"
WHERE value_text IS NOT NULL
