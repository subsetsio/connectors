SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_site" AS VARCHAR) AS "id_site",
    CAST("number_features" AS VARCHAR) AS "number_features",
    CAST("number_habitats" AS VARCHAR) AS "number_habitats",
    CAST("number_species" AS VARCHAR) AS "number_species",
    CAST("site_name" AS VARCHAR) AS "site_name"
FROM "european-environment-agency-bise.country-emerald-number-species-habitats"
