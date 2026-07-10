SELECT
    CAST("Action" AS VARCHAR) AS "Action",
    CAST("Action_Id" AS VARCHAR) AS "Action_Id",
    CAST("Co_Benefits_Label" AS VARCHAR) AS "Co_Benefits_Label",
    CAST("Funding_Sources" AS VARCHAR) AS "Funding_Sources",
    CAST("Funding_Sources_Label" AS VARCHAR) AS "Funding_Sources_Label",
    CAST("Hazards_Addressed_Label" AS VARCHAR) AS "Hazards_Addressed_Label",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("More_Details_Label" AS VARCHAR) AS "More_Details_Label",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Sectors_Label" AS VARCHAR) AS "Sectors_Label",
    CAST("Signatory" AS VARCHAR) AS "Signatory"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-action-template-actions-text"
