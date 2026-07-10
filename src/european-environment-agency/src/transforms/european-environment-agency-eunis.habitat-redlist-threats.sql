SELECT
    CAST("description" AS VARCHAR) AS "description",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("main_threat" AS VARCHAR) AS "main_threat",
    CAST("sort_order" AS VARCHAR) AS "sort_order",
    CAST("threat_code" AS VARCHAR) AS "threat_code"
FROM "european-environment-agency-eunis.habitat-redlist-threats"
