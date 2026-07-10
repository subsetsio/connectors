SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("habitat_category" AS VARCHAR) AS "habitat_category",
    CAST("habitat_description" AS VARCHAR) AS "habitat_description",
    CAST("habitat_prioriy" AS VARCHAR) AS "habitat_prioriy",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("number_countries" AS VARCHAR) AS "number_countries",
    CAST("number_sites" AS VARCHAR) AS "number_sites",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name"
FROM "european-environment-agency-bise.habitat-information"
