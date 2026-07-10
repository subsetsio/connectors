SELECT
    CAST("EEAActivity" AS VARCHAR) AS "EEAActivity",
    CAST("EEASector" AS VARCHAR) AS "EEASector",
    CAST("EEASubSector" AS VARCHAR) AS "EEASubSector",
    CAST("eprtrActivityCode" AS VARCHAR) AS "eprtrActivityCode",
    CAST("eprtrActivityName" AS VARCHAR) AS "eprtrActivityName",
    CAST("eprtrAnnexIActivity" AS VARCHAR) AS "eprtrAnnexIActivity",
    CAST("eprtrSectorName" AS VARCHAR) AS "eprtrSectorName",
    CAST("eprtrSectorNameLabel" AS VARCHAR) AS "eprtrSectorNameLabel",
    CAST("Id" AS VARCHAR) AS "Id"
FROM "european-environment-agency-ied.eprtr-sectors"
