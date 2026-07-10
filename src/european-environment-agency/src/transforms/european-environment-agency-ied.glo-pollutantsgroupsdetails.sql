SELECT
    CAST("code" AS VARCHAR) AS "code",
    CAST("codeEPER" AS VARCHAR) AS "codeEPER",
    CAST("description" AS VARCHAR) AS "description",
    CAST("name" AS VARCHAR) AS "name",
    CAST("pollutant_group_id" AS VARCHAR) AS "pollutant_group_id",
    CAST("startYear" AS VARCHAR) AS "startYear",
    CAST("sub" AS VARCHAR) AS "sub"
FROM "european-environment-agency-ied.glo-pollutantsgroupsdetails"
