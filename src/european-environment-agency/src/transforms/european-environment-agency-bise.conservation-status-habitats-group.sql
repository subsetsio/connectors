SELECT
    CAST("assessment_Bad" AS VARCHAR) AS "assessment_Bad",
    CAST("assessment_Good" AS VARCHAR) AS "assessment_Good",
    CAST("assessment_Poor" AS VARCHAR) AS "assessment_Poor",
    CAST("assessment_total" AS VARCHAR) AS "assessment_total",
    CAST("assessment_Unknown" AS VARCHAR) AS "assessment_Unknown",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("Habitats_Group" AS VARCHAR) AS "Habitats_Group",
    CAST("Latest_Discodata_update" AS VARCHAR) AS "Latest_Discodata_update",
    CAST("Percentage_Bad" AS VARCHAR) AS "Percentage_Bad",
    CAST("Percentage_Good" AS VARCHAR) AS "Percentage_Good",
    CAST("Percentage_Poor" AS VARCHAR) AS "Percentage_Poor",
    CAST("Percentage_total" AS VARCHAR) AS "Percentage_total",
    CAST("Percentage_Unknown" AS VARCHAR) AS "Percentage_Unknown"
FROM "european-environment-agency-bise.conservation-status-habitats-group"
