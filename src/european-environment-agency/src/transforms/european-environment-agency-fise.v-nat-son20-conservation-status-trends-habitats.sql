SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("deteriorating" AS VARCHAR) AS "deteriorating",
    CAST("deteriorating_percentage" AS VARCHAR) AS "deteriorating_percentage",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("habitat_group_with_total" AS VARCHAR) AS "habitat_group_with_total",
    CAST("habitats" AS VARCHAR) AS "habitats",
    CAST("improving" AS VARCHAR) AS "improving",
    CAST("improving_percentage" AS VARCHAR) AS "improving_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("stable" AS VARCHAR) AS "stable",
    CAST("stable_percentage" AS VARCHAR) AS "stable_percentage",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-conservation-status-trends-habitats"
