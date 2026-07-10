SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("internationalRBD" AS VARCHAR) AS "internationalRBD",
    CAST("internationalRBDName" AS VARCHAR) AS "internationalRBDName",
    CAST("primeCompetentAuthority" AS VARCHAR) AS "primeCompetentAuthority",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("subUnitsDefined" AS VARCHAR) AS "subUnitsDefined"
FROM "european-environment-agency-wise-wfd.rbdsuca-rbd-primecompetentauthority"
