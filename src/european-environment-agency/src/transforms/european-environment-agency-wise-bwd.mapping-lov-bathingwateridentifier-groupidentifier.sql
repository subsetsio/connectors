SELECT
    CAST("bathingWaterIdentifier" AS VARCHAR) AS "bathingWaterIdentifier",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("fromSeason" AS VARCHAR) AS "fromSeason",
    CAST("groupIdentifier" AS VARCHAR) AS "groupIdentifier",
    CAST("toSeason" AS VARCHAR) AS "toSeason"
FROM "european-environment-agency-wise-bwd.mapping-lov-bathingwateridentifier-groupidentifier"
