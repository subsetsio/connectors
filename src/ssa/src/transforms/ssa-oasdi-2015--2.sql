SELECT
    CAST("State_Territory" AS VARCHAR) AS state,
    2015 AS year,
    CAST("Total_Population" AS BIGINT) AS total_population,
    CAST("Total_Population_Receiving_Bene" AS DOUBLE) AS total_population_receiving_benefits,
    CAST("Population65_Older" AS BIGINT) AS population_65_older,
    CAST("Population65_Older_Receiving_Be" AS DOUBLE) AS population_65_older_receiving_benefits
FROM "ssa-oasdi-2015--2"
WHERE "State_Territory" IS NOT NULL AND TRIM(CAST("State_Territory" AS VARCHAR)) <> ''
