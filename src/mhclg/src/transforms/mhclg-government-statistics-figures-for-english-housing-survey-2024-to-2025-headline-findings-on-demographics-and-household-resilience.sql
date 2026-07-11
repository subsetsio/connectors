SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-figures-for-english-housing-survey-2024-to-2025-headline-findings-on-demographics-and-household-resilience"
WHERE n_cols > 0
