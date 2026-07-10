SELECT
    CAST("numberTrees" AS VARCHAR) AS "numberTrees",
    CAST("NUTS3_region" AS VARCHAR) AS "NUTS3_region",
    CAST("organisationCode" AS VARCHAR) AS "organisationCode",
    CAST("organisationID" AS VARCHAR) AS "organisationID",
    CAST("pledgeID" AS VARCHAR) AS "pledgeID",
    CAST("pledgeName" AS VARCHAR) AS "pledgeName",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-mapmytree.v-pledge-catalogue"
