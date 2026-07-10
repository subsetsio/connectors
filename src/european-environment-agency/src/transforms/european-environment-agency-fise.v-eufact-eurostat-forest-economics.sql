SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("gross_value_added" AS VARCHAR) AS "gross_value_added",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("output_of_forestry_and_connected_secondary_activities" AS VARCHAR) AS "output_of_forestry_and_connected_secondary_activities",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-eufact-eurostat-forest-economics"
