SELECT
    CAST("Action_Id" AS VARCHAR) AS "Action_Id",
    CAST("Climate_Hazard" AS VARCHAR) AS "Climate_Hazard",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Signatory" AS VARCHAR) AS "Signatory"
FROM "european-environment-agency-missiononadaptation.v-action-template-climate-hazards-text"
