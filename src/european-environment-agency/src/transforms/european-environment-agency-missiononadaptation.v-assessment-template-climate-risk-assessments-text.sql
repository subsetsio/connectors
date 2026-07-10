SELECT
    CAST("Assessment_Id" AS VARCHAR) AS "Assessment_Id",
    CAST("Attachment" AS VARCHAR) AS "Attachment",
    CAST("Attachment_Title" AS VARCHAR) AS "Attachment_Title",
    CAST("DirectLink" AS VARCHAR) AS "DirectLink",
    CAST("Explore_Link_Text" AS VARCHAR) AS "Explore_Link_Text",
    CAST("Factors" AS VARCHAR) AS "Factors",
    CAST("Further_Details_Label" AS VARCHAR) AS "Further_Details_Label",
    CAST("Hyperlink" AS VARCHAR) AS "Hyperlink",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("IsLocalFile" AS VARCHAR) AS "IsLocalFile",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Please_Explain" AS VARCHAR) AS "Please_Explain",
    CAST("Signatory" AS VARCHAR) AS "Signatory",
    CAST("Year_Of_Publication" AS VARCHAR) AS "Year_Of_Publication",
    CAST("Year_Of_Publication_Label" AS VARCHAR) AS "Year_Of_Publication_Label"
FROM "european-environment-agency-missiononadaptation.v-assessment-template-climate-risk-assessments-text"
