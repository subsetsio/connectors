SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("deteriorating" AS VARCHAR) AS "deteriorating",
    CAST("deteriorating_percentage" AS VARCHAR) AS "deteriorating_percentage",
    CAST("improving" AS VARCHAR) AS "improving",
    CAST("improving_percentage" AS VARCHAR) AS "improving_percentage",
    CAST("label" AS VARCHAR) AS "label",
    CAST("label_with_total" AS VARCHAR) AS "label_with_total",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("stable" AS VARCHAR) AS "stable",
    CAST("stable_percentage" AS VARCHAR) AS "stable_percentage",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-6-15-trends-in-status-of-forest-non-bird-and-bird-species"
