SELECT
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("main_category" AS VARCHAR) AS "main_category",
    CAST("subcategory" AS VARCHAR) AS "subcategory"
FROM "european-environment-agency-eunis.habitat-redlist-conservation"
