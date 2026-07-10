SELECT
    CAST("Forestry_economic_accounts" AS VARCHAR) AS "Forestry_economic_accounts",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.eurostat-value-added-tag00058"
