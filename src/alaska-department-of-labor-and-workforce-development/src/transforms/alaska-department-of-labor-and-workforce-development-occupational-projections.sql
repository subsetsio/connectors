SELECT CAST(occupation_code AS VARCHAR) AS occupation_code, occupation_title,
       CAST(base_year AS INTEGER) AS base_year,
       CAST(projected_year AS INTEGER) AS projected_year,
       CAST(base_employment AS BIGINT) AS base_employment,
       CAST(projected_employment AS BIGINT) AS projected_employment,
       CAST(numeric_change AS BIGINT) AS numeric_change,
       CAST(percent_change AS DOUBLE) AS percent_change,
       CAST(labor_force_exits AS DOUBLE) AS labor_force_exits,
       CAST(occupational_transfers AS DOUBLE) AS occupational_transfers,
       CAST(total_separations AS DOUBLE) AS total_separations,
       CAST(annual_openings AS DOUBLE) AS annual_openings,
       CAST(mean_hourly_wage AS DOUBLE) AS mean_hourly_wage
FROM "alaska-department-of-labor-and-workforce-development-occupational-projections"
WHERE occupation_title IS NOT NULL
