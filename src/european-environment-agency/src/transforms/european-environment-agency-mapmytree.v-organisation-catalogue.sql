SELECT
    CAST("countries" AS VARCHAR) AS "countries",
    CAST("description" AS VARCHAR) AS "description",
    CAST("email" AS VARCHAR) AS "email",
    CAST("isUmbrella" AS VARCHAR) AS "isUmbrella",
    CAST("logo" AS VARCHAR) AS "logo",
    CAST("logoPublicPath" AS VARCHAR) AS "logoPublicPath",
    CAST("name" AS VARCHAR) AS "name",
    CAST("organisationCode" AS VARCHAR) AS "organisationCode",
    CAST("organisationID" AS VARCHAR) AS "organisationID",
    CAST("totalPledges" AS VARCHAR) AS "totalPledges",
    CAST("totalTrees" AS VARCHAR) AS "totalTrees",
    CAST("website" AS VARCHAR) AS "website"
FROM "european-environment-agency-mapmytree.v-organisation-catalogue"
