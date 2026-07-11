SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistics-english-housing-survey-2023-to-2024-understanding-housing-circumstances-a-multivariate-analysis"
WHERE n_cols > 0
