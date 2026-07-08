SELECT industry, CAST(naics_code AS VARCHAR) AS naics_code,
       CAST(year AS INTEGER) AS year, case_type,
       CAST(incidence_rate AS DOUBLE) AS incidence_rate
FROM "alaska-department-of-labor-and-workforce-development-nonfatal-injuries-illnesses"
WHERE industry IS NOT NULL AND incidence_rate IS NOT NULL
