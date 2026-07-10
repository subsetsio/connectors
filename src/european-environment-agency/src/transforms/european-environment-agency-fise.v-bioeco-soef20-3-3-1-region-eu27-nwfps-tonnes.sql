SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("total_harvested_non_wood_goods_unit" AS VARCHAR) AS "total_harvested_non_wood_goods_unit",
    CAST("total_tones" AS VARCHAR) AS "total_tones"
FROM "european-environment-agency-fise.v-bioeco-soef20-3-3-1-region-eu27-nwfps-tonnes"
