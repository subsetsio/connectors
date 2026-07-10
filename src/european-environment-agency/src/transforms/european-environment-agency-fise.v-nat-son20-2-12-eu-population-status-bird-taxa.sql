SELECT
    CAST("favourable" AS VARCHAR) AS "favourable",
    CAST("favourable_percentage" AS VARCHAR) AS "favourable_percentage",
    CAST("label" AS VARCHAR) AS "label",
    CAST("label_with_total" AS VARCHAR) AS "label_with_total",
    CAST("unfavourable_bad" AS VARCHAR) AS "unfavourable_bad",
    CAST("unfavourable_bad_percentage" AS VARCHAR) AS "unfavourable_bad_percentage",
    CAST("unfavourable_inadequate" AS VARCHAR) AS "unfavourable_inadequate",
    CAST("unfavourable_inadequate_percentage" AS VARCHAR) AS "unfavourable_inadequate_percentage",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-2-12-eu-population-status-bird-taxa"
