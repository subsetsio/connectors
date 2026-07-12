SELECT
    CAST("State" AS VARCHAR) AS state,
    2013 AS year,
    CAST("Total_population_number_thousan" AS BIGINT) AS total_population,
    CAST("Total_population_percentage_rec" AS DOUBLE) AS total_population_receiving_benefits,
    CAST("Population_aged65_or_older_numb" AS BIGINT) AS population_65_older,
    CAST("Population_aged65_or_older_perc" AS DOUBLE) AS population_65_older_receiving_benefits
FROM "ssa-oasdi--2013--0"
WHERE "State" IS NOT NULL AND TRIM(CAST("State" AS VARCHAR)) <> ''
