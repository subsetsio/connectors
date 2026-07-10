SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("favourable" AS VARCHAR) AS "favourable",
    CAST("favourable_percentage" AS VARCHAR) AS "favourable_percentage",
    CAST("habitat_group_with_total" AS VARCHAR) AS "habitat_group_with_total",
    CAST("habitats" AS VARCHAR) AS "habitats",
    CAST("not_applied" AS VARCHAR) AS "not_applied",
    CAST("not_applied_percentage" AS VARCHAR) AS "not_applied_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("region_name" AS VARCHAR) AS "region_name",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unfavourable_bad" AS VARCHAR) AS "unfavourable_bad",
    CAST("unfavourable_bad_percentage" AS VARCHAR) AS "unfavourable_bad_percentage",
    CAST("unfavourable_inadequate" AS VARCHAR) AS "unfavourable_inadequate",
    CAST("unfavourable_inadequate_percentage" AS VARCHAR) AS "unfavourable_inadequate_percentage",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-conservation-status-habitats-by-region"
