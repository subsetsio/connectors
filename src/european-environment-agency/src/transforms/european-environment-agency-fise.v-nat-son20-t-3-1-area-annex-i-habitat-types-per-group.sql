SELECT
    CAST("% of Annex I" AS VARCHAR) AS "% of Annex I",
    CAST("Average area (Mha)" AS VARCHAR) AS "Average area (Mha)",
    CAST("country" AS VARCHAR) AS "country",
    CAST("EUNIS habitat group" AS VARCHAR) AS "EUNIS habitat group",
    CAST("habitat_order" AS VARCHAR) AS "habitat_order",
    CAST("habitats" AS VARCHAR) AS "habitats",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units"
FROM "european-environment-agency-fise.v-nat-son20-t-3-1-area-annex-i-habitat-types-per-group"
