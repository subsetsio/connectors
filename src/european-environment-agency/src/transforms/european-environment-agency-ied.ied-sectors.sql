SELECT
    CAST("definition" AS VARCHAR) AS "definition",
    CAST("EEAActivity" AS VARCHAR) AS "EEAActivity",
    CAST("EEASector" AS VARCHAR) AS "EEASector",
    CAST("EEASubSector" AS VARCHAR) AS "EEASubSector",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("notation" AS VARCHAR) AS "notation"
FROM "european-environment-agency-ied.ied-sectors"
