SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("GDP" AS VARCHAR) AS "GDP",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.ghg-eustat-gdp"
