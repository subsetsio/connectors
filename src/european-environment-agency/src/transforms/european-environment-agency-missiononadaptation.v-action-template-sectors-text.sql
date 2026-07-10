SELECT
    CAST("Action_Id" AS VARCHAR) AS "Action_Id",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Sector" AS VARCHAR) AS "Sector",
    CAST("Signatory" AS VARCHAR) AS "Signatory"
FROM "european-environment-agency-missiononadaptation.v-action-template-sectors-text"
