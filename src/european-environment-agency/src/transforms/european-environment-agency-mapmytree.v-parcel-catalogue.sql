SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("lat" AS VARCHAR) AS "lat",
    CAST("long" AS VARCHAR) AS "long",
    CAST("numberTrees" AS VARCHAR) AS "numberTrees",
    CAST("organisationCode" AS VARCHAR) AS "organisationCode",
    CAST("organisationID" AS VARCHAR) AS "organisationID",
    CAST("organisationName" AS VARCHAR) AS "organisationName",
    CAST("parcelID" AS VARCHAR) AS "parcelID",
    CAST("pledgeID" AS VARCHAR) AS "pledgeID",
    CAST("pledgeName" AS VARCHAR) AS "pledgeName"
FROM "european-environment-agency-mapmytree.v-parcel-catalogue"
