SELECT CAST(area_code AS VARCHAR) AS area_code, area_name,
       CAST(naics_code AS VARCHAR) AS naics_code, naics_description,
       CAST(year AS INTEGER) AS year, CAST(ownership AS VARCHAR) AS ownership,
       CAST(establishments AS BIGINT) AS establishments,
       CAST(avg_employment AS DOUBLE) AS avg_employment,
       CAST(total_wages AS BIGINT) AS total_wages,
       CAST(avg_monthly_wage AS DOUBLE) AS avg_monthly_wage
FROM "alaska-department-of-labor-and-workforce-development-qcew"
WHERE naics_code IS NOT NULL AND year IS NOT NULL
