SELECT category AS destination_country, series AS project_status,
       TRY_CAST(value AS DOUBLE) AS investment_eur
FROM "bruegel-european-clean-tech-tracker" WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
