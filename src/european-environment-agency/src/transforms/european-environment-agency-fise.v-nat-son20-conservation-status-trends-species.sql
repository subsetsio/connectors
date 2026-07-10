SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("deteriorating" AS VARCHAR) AS "deteriorating",
    CAST("deteriorating_percentage" AS VARCHAR) AS "deteriorating_percentage",
    CAST("improving" AS VARCHAR) AS "improving",
    CAST("improving_percentage" AS VARCHAR) AS "improving_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("species" AS VARCHAR) AS "species",
    CAST("stable" AS VARCHAR) AS "stable",
    CAST("stable_percentage" AS VARCHAR) AS "stable_percentage",
    CAST("taxGroup" AS VARCHAR) AS "taxGroup",
    CAST("taxgroup_with_total" AS VARCHAR) AS "taxgroup_with_total",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-conservation-status-trends-species"
