SELECT
    CAST("CNTR_CODE" AS VARCHAR) AS "CNTR_CODE",
    CAST("CNTR_NAME" AS VARCHAR) AS "CNTR_NAME",
    CAST("UNIT" AS VARCHAR) AS "UNIT",
    CAST("VALUE_65_YEAR" AS VARCHAR) AS "VALUE_65_YEAR",
    CAST("VALUE_UNDER_1" AS VARCHAR) AS "VALUE_UNDER_1",
    CAST("YEAR" AS VARCHAR) AS "YEAR"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-adaptationdashboard-heat-exposure-people"
