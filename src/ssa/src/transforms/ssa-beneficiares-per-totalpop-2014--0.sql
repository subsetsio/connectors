SELECT
    CAST("State" AS VARCHAR) AS state,
    2014 AS year,
    CAST("Total_Pop_" AS BIGINT) AS total_population,
    CAST("TP_Benefit" AS DOUBLE) AS total_population_receiving_benefits,
    CAST("Pop_gte65_" AS BIGINT) AS population_65_older,
    CAST("gte65_Bene" AS DOUBLE) AS population_65_older_receiving_benefits
FROM "ssa-beneficiares-per-totalpop-2014--0"
WHERE "State" IS NOT NULL AND TRIM(CAST("State" AS VARCHAR)) <> ''
