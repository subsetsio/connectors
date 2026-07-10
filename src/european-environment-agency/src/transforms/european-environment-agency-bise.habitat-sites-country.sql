SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("number_sites" AS VARCHAR) AS "number_sites"
FROM "european-environment-agency-bise.habitat-sites-country"
