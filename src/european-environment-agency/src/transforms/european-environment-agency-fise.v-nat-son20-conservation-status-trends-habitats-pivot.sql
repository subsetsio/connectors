SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("habitat_group_with_total" AS VARCHAR) AS "habitat_group_with_total",
    CAST("habitats" AS VARCHAR) AS "habitats",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("status" AS VARCHAR) AS "status",
    CAST("status_label" AS VARCHAR) AS "status_label",
    CAST("status_order" AS VARCHAR) AS "status_order",
    CAST("value" AS VARCHAR) AS "value"
FROM "european-environment-agency-fise.v-nat-son20-conservation-status-trends-habitats-pivot"
