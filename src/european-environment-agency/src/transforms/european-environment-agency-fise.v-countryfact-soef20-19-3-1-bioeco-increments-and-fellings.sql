SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("Fellings_percentage_net_increment" AS VARCHAR) AS "Fellings_percentage_net_increment",
    CAST("fellings_total" AS VARCHAR) AS "fellings_total",
    CAST("gross_annual_increment" AS VARCHAR) AS "gross_annual_increment",
    CAST("nai_after_fellings" AS VARCHAR) AS "nai_after_fellings",
    CAST("net_annual_increment" AS VARCHAR) AS "net_annual_increment",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-countryfact-soef20-19-3-1-bioeco-increments-and-fellings"
