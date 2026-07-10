SELECT
    CAST("Abstract" AS VARCHAR) AS "Abstract",
    CAST("Ad_Hyperlink_Introduction" AS VARCHAR) AS "Ad_Hyperlink_Introduction",
    CAST("Ad_Hyperlink_Text" AS VARCHAR) AS "Ad_Hyperlink_Text",
    CAST("Ad_Hyperlink_Title" AS VARCHAR) AS "Ad_Hyperlink_Title",
    CAST("Attachments" AS VARCHAR) AS "Attachments",
    CAST("ClimateRiskAssesmentExists" AS VARCHAR) AS "ClimateRiskAssesmentExists",
    CAST("Cra_Abstract" AS VARCHAR) AS "Cra_Abstract",
    CAST("Cra_Title" AS VARCHAR) AS "Cra_Title",
    CAST("Hazards_Abstract" AS VARCHAR) AS "Hazards_Abstract",
    CAST("Hazards_Title" AS VARCHAR) AS "Hazards_Title",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Signatory" AS VARCHAR) AS "Signatory",
    CAST("Subheading" AS VARCHAR) AS "Subheading",
    CAST("Title" AS VARCHAR) AS "Title"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-assessment-template-text"
