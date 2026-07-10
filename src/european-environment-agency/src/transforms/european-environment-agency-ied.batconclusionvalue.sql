SELECT
    CAST("AcceptedDate" AS VARCHAR) AS "AcceptedDate",
    CAST("Definition" AS VARCHAR) AS "Definition",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Label" AS VARCHAR) AS "Label",
    CAST("Notation" AS VARCHAR) AS "Notation",
    CAST("Status" AS VARCHAR) AS "Status",
    CAST("StatusModifiedYear" AS VARCHAR) AS "StatusModifiedYear",
    CAST("URI" AS VARCHAR) AS "URI"
FROM "european-environment-agency-ied.batconclusionvalue"
