SELECT
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("furtherDetails" AS VARCHAR) AS "furtherDetails",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("methodClassification" AS VARCHAR) AS "methodClassification",
    CAST("offsiteWasteTransferId" AS VARCHAR) AS "offsiteWasteTransferId"
FROM "european-environment-agency-ied.offsitewastetransfermethodclassification"
