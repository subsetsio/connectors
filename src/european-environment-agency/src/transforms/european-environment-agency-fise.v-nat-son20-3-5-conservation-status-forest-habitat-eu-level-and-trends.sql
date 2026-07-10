SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("favourable" AS VARCHAR) AS "favourable",
    CAST("favourable_percentage" AS VARCHAR) AS "favourable_percentage",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("not_applied" AS VARCHAR) AS "not_applied",
    CAST("not_applied_percentage" AS VARCHAR) AS "not_applied_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("species" AS VARCHAR) AS "species",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unfavourable_bad" AS VARCHAR) AS "unfavourable_bad",
    CAST("unfavourable_bad_percentage" AS VARCHAR) AS "unfavourable_bad_percentage",
    CAST("unfavourable_inadequate" AS VARCHAR) AS "unfavourable_inadequate",
    CAST("unfavourable_inadequate_percentage" AS VARCHAR) AS "unfavourable_inadequate_percentage",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-3-5-conservation-status-forest-habitat-eu-level-and-trends"
