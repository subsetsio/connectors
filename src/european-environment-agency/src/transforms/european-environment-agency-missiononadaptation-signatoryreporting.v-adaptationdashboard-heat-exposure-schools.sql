SELECT
    CAST("CNTR_CODE" AS VARCHAR) AS "CNTR_CODE",
    CAST("CNTR_NAME" AS VARCHAR) AS "CNTR_NAME",
    CAST("IND_VALUE" AS VARCHAR) AS "IND_VALUE",
    CAST("NUTS2" AS VARCHAR) AS "NUTS2",
    CAST("NUTS2_NAME" AS VARCHAR) AS "NUTS2_NAME",
    CAST("UNIT" AS VARCHAR) AS "UNIT",
    CAST("YEAR" AS VARCHAR) AS "YEAR"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-adaptationdashboard-heat-exposure-schools"
