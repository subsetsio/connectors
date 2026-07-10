SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("number_sites" AS VARCHAR) AS "number_sites",
    CAST("species_group" AS VARCHAR) AS "species_group",
    CAST("species_name" AS VARCHAR) AS "species_name"
FROM "european-environment-agency-bise.country-top-5-species-more-sites"
