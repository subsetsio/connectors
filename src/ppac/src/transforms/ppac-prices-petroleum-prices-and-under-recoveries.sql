SELECT sheet,
       row_number,
       column_number,
       cell_text,
       CAST(cell_number AS DOUBLE) AS cell_number
FROM "ppac-prices-petroleum-prices-and-under-recoveries"
WHERE cell_text IS NOT NULL OR cell_number IS NOT NULL
