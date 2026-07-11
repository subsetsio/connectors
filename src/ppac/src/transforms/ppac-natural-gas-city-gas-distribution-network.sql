SELECT sheet,
       row_number,
       column_number,
       cell_text,
       CAST(cell_number AS DOUBLE) AS cell_number
FROM "ppac-natural-gas-city-gas-distribution-network"
WHERE cell_text IS NOT NULL OR cell_number IS NOT NULL
