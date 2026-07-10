SELECT
    CAST("Adaptation_Goal_Id" AS VARCHAR) AS "Adaptation_Goal_Id",
    CAST("Climate_Action_Abstract" AS VARCHAR) AS "Climate_Action_Abstract",
    CAST("Climate_Action_Title" AS VARCHAR) AS "Climate_Action_Title",
    CAST("Climate_Hazards_Addressed_Label" AS VARCHAR) AS "Climate_Hazards_Addressed_Label",
    CAST("Comments" AS VARCHAR) AS "Comments",
    CAST("Comments_Label" AS VARCHAR) AS "Comments_Label",
    CAST("Description" AS VARCHAR) AS "Description",
    CAST("Description_Label" AS VARCHAR) AS "Description_Label",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("More_Details_Label" AS VARCHAR) AS "More_Details_Label",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Signatory" AS VARCHAR) AS "Signatory",
    CAST("Title" AS VARCHAR) AS "Title",
    CAST("Title_Label" AS VARCHAR) AS "Title_Label"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-planning-template-adaptation-goals-text"
