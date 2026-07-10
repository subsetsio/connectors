SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("favourable" AS VARCHAR) AS "favourable",
    CAST("favourable_percentage" AS VARCHAR) AS "favourable_percentage",
    CAST("not_applied" AS VARCHAR) AS "not_applied",
    CAST("not_applied_percentage" AS VARCHAR) AS "not_applied_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("region_name" AS VARCHAR) AS "region_name",
    CAST("region_name_with_total" AS VARCHAR) AS "region_name_with_total",
    CAST("species" AS VARCHAR) AS "species",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unfavourable_bad" AS VARCHAR) AS "unfavourable_bad",
    CAST("unfavourable_bad_percentage" AS VARCHAR) AS "unfavourable_bad_percentage",
    CAST("unfavourable_inadequate" AS VARCHAR) AS "unfavourable_inadequate",
    CAST("unfavourable_inadequate_percentage" AS VARCHAR) AS "unfavourable_inadequate_percentage",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-conservation-status-species-by-region"
