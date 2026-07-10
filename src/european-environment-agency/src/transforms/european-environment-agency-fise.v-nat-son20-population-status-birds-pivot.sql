SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("label" AS VARCHAR) AS "label",
    CAST("label_with_total" AS VARCHAR) AS "label_with_total",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("status" AS VARCHAR) AS "status",
    CAST("status_label" AS VARCHAR) AS "status_label",
    CAST("status_order" AS VARCHAR) AS "status_order",
    CAST("value" AS VARCHAR) AS "value"
FROM "european-environment-agency-fise.v-nat-son20-population-status-birds-pivot"
