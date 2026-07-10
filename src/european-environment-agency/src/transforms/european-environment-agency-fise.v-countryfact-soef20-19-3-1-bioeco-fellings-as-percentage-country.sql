SELECT
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("felling" AS VARCHAR) AS "felling",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("percentage" AS VARCHAR) AS "percentage",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-countryfact-soef20-19-3-1-bioeco-fellings-as-percentage-country"
