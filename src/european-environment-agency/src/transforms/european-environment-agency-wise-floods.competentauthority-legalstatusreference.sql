SELECT
    CAST("acronym" AS VARCHAR) AS "acronym",
    CAST("competentAuthorityName" AS VARCHAR) AS "competentAuthorityName",
    CAST("competentAuthorityNameNL" AS VARCHAR) AS "competentAuthorityNameNL",
    CAST("competentAuthorityNameNLLanguage" AS VARCHAR) AS "competentAuthorityNameNLLanguage",
    CAST("country" AS VARCHAR) AS "country",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euCACode" AS VARCHAR) AS "euCACode",
    CAST("legalStatusReference" AS VARCHAR) AS "legalStatusReference",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("url" AS VARCHAR) AS "url"
FROM "european-environment-agency-wise-floods.competentauthority-legalstatusreference"
