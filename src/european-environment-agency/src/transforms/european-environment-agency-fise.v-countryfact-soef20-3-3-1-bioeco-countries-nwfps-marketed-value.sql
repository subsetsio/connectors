SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("currency" AS VARCHAR) AS "currency",
    CAST("currency_local" AS VARCHAR) AS "currency_local",
    CAST("isTotal" AS VARCHAR) AS "isTotal",
    CAST("Marketed_value" AS VARCHAR) AS "Marketed_value",
    CAST("Marketed_value_local" AS VARCHAR) AS "Marketed_value_local",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("nwfp_category" AS VARCHAR) AS "nwfp_category"
FROM "european-environment-agency-fise.v-countryfact-soef20-3-3-1-bioeco-countries-nwfps-marketed-value"
