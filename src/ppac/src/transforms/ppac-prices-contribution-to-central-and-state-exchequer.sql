SELECT sheet,
       row_number,
       column_number,
       cell_text,
       CAST(cell_number AS DOUBLE) AS cell_number
FROM "ppac-prices-contribution-to-central-and-state-exchequer"
WHERE cell_text IS NOT NULL OR cell_number IS NOT NULL
