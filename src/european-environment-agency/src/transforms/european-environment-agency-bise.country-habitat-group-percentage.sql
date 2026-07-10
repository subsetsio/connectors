SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("group_percentage" AS VARCHAR) AS "group_percentage",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("number_habitats" AS VARCHAR) AS "number_habitats"
FROM "european-environment-agency-bise.country-habitat-group-percentage"
