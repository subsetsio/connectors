SELECT
    CAST("comment" AS VARCHAR) AS "comment",
    CAST("country" AS VARCHAR) AS "country",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("inventory_year" AS VARCHAR) AS "inventory_year",
    CAST("isCalculatedByEEA" AS VARCHAR) AS "isCalculatedByEEA",
    CAST("notation" AS VARCHAR) AS "notation",
    CAST("submission_version" AS VARCHAR) AS "submission_version",
    CAST("value" AS VARCHAR) AS "value",
    CAST("variable_uid" AS VARCHAR) AS "variable_uid"
FROM "european-environment-agency-ghg-inventory.ghg-value"
