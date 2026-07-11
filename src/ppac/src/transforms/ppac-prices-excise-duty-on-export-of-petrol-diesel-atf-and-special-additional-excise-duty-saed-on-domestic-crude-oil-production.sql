SELECT sheet,
       row_number,
       column_number,
       cell_text,
       CAST(cell_number AS DOUBLE) AS cell_number
FROM "ppac-prices-excise-duty-on-export-of-petrol-diesel-atf-and-special-additional-excise-duty-saed-on-domestic-crude-oil-production"
WHERE cell_text IS NOT NULL OR cell_number IS NOT NULL
