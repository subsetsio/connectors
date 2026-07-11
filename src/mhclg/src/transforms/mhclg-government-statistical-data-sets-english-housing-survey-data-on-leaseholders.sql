SELECT
    attachment_filename,
    attachment_title,
    content_type,
    sheet_name,
    CAST(row_index AS BIGINT) AS row_index,
    CAST(n_cols AS BIGINT) AS n_cols,
    cells
FROM "mhclg-government-statistical-data-sets-english-housing-survey-data-on-leaseholders"
WHERE n_cols > 0
