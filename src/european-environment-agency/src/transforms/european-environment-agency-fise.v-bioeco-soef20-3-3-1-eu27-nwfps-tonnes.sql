SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("nwfp_category" AS VARCHAR) AS "nwfp_category",
    CAST("nwfp_category_short" AS VARCHAR) AS "nwfp_category_short",
    CAST("total_tonnes" AS VARCHAR) AS "total_tonnes",
    CAST("units" AS VARCHAR) AS "units"
FROM "european-environment-agency-fise.v-bioeco-soef20-3-3-1-eu27-nwfps-tonnes"
