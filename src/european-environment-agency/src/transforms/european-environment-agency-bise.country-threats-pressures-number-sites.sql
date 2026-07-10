SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("impact_code" AS VARCHAR) AS "impact_code",
    CAST("impact_description" AS VARCHAR) AS "impact_description",
    CAST("number_sites" AS VARCHAR) AS "number_sites"
FROM "european-environment-agency-bise.country-threats-pressures-number-sites"
