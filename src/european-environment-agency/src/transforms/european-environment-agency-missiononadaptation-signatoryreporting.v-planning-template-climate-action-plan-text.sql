SELECT
    CAST("Approval_Year" AS VARCHAR) AS "Approval_Year",
    CAST("Attachment" AS VARCHAR) AS "Attachment",
    CAST("Climate_Action_Plan_Id" AS VARCHAR) AS "Climate_Action_Plan_Id",
    CAST("Description" AS VARCHAR) AS "Description",
    CAST("End_Year" AS VARCHAR) AS "End_Year",
    CAST("End_Year_Of_Plan_Label" AS VARCHAR) AS "End_Year_Of_Plan_Label",
    CAST("Explore_Plan_Link_Text" AS VARCHAR) AS "Explore_Plan_Link_Text",
    CAST("Further_Information_Link_Text" AS VARCHAR) AS "Further_Information_Link_Text",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Name_Of_Plan_And_Hyperlink" AS VARCHAR) AS "Name_Of_Plan_And_Hyperlink",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Sectors_Introduction" AS VARCHAR) AS "Sectors_Introduction",
    CAST("Signatory" AS VARCHAR) AS "Signatory",
    CAST("Type" AS VARCHAR) AS "Type",
    CAST("Year_Of_Approval_Label" AS VARCHAR) AS "Year_Of_Approval_Label"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-planning-template-climate-action-plan-text"
