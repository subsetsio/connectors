SELECT
    CAST("cas" AS VARCHAR) AS "cas",
    CAST("code" AS VARCHAR) AS "code",
    CAST("codeEPER" AS VARCHAR) AS "codeEPER",
    CAST("endYear" AS VARCHAR) AS "endYear",
    CAST("eperPollutantId" AS VARCHAR) AS "eperPollutantId",
    CAST("name" AS VARCHAR) AS "name",
    CAST("parentId" AS VARCHAR) AS "parentId",
    CAST("pollutantId" AS VARCHAR) AS "pollutantId",
    CAST("startYear" AS VARCHAR) AS "startYear"
FROM "european-environment-agency-ied.glo-pollutants"
