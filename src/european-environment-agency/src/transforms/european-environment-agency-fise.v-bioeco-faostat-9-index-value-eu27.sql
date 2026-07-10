SELECT
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("IndexValue" AS VARCHAR) AS "IndexValue",
    CAST("Item" AS VARCHAR) AS "Item",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("Value" AS VARCHAR) AS "Value",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-bioeco-faostat-9-index-value-eu27"
