SELECT
    CAST("acronym" AS VARCHAR) AS "acronym",
    CAST("city" AS VARCHAR) AS "city",
    CAST("cityNL" AS VARCHAR) AS "cityNL",
    CAST("competentAuthorityName" AS VARCHAR) AS "competentAuthorityName",
    CAST("competentAuthorityNameNL" AS VARCHAR) AS "competentAuthorityNameNL",
    CAST("competentAuthorityNameNLLanguage" AS VARCHAR) AS "competentAuthorityNameNLLanguage",
    CAST("country" AS VARCHAR) AS "country",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euCACode" AS VARCHAR) AS "euCACode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("linkToCompetentAuthority" AS VARCHAR) AS "linkToCompetentAuthority",
    CAST("otherRole" AS VARCHAR) AS "otherRole",
    CAST("postcode" AS VARCHAR) AS "postcode",
    CAST("street" AS VARCHAR) AS "street"
FROM "european-environment-agency-wise-wfd.rbdsuca-competentauthority-otherrole"
