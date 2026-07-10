SELECT
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("country_type" AS VARCHAR) AS "country_type",
    CAST("current_area_value" AS VARCHAR) AS "current_area_value",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("present" AS VARCHAR) AS "present",
    CAST("sea_name" AS VARCHAR) AS "sea_name",
    CAST("trend_quality" AS VARCHAR) AS "trend_quality",
    CAST("trend_quantity" AS VARCHAR) AS "trend_quantity"
FROM "european-environment-agency-eunis.habitat-redlist-occurrence"
