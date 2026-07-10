SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("url" AS VARCHAR) AS "url",
    CAST("wfdCompetentAuthorities" AS VARCHAR) AS "wfdCompetentAuthorities",
    CAST("wfdRiverBasinDistricts" AS VARCHAR) AS "wfdRiverBasinDistricts"
FROM "european-environment-agency-wise-floods.wfdcompetentauthoritiesanduoms"
