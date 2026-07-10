SELECT
    CAST("AcceptedDate" AS VARCHAR) AS "AcceptedDate",
    CAST("code" AS VARCHAR) AS "code",
    CAST("Definition" AS VARCHAR) AS "Definition",
    CAST("Label" AS VARCHAR) AS "Label",
    CAST("Notation" AS VARCHAR) AS "Notation",
    CAST("Status" AS VARCHAR) AS "Status",
    CAST("URI" AS VARCHAR) AS "URI"
FROM "european-environment-agency-ied.eprtrannexiactivityvalue"
