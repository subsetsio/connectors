SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("group_percentage" AS VARCHAR) AS "group_percentage",
    CAST("number_species" AS VARCHAR) AS "number_species",
    CAST("species_group" AS VARCHAR) AS "species_group"
FROM "european-environment-agency-bise.country-species-group-percentage"
