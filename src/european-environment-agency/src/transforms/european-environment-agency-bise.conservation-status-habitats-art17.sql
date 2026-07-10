SELECT
    CAST("Count_assessment_Bad" AS VARCHAR) AS "Count_assessment_Bad",
    CAST("Count_assessment_Good" AS VARCHAR) AS "Count_assessment_Good",
    CAST("Count_assessment_Poor" AS VARCHAR) AS "Count_assessment_Poor",
    CAST("Count_assessment_total" AS VARCHAR) AS "Count_assessment_total",
    CAST("Count_assessment_Unknown" AS VARCHAR) AS "Count_assessment_Unknown",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("Latest_discodata_update" AS VARCHAR) AS "Latest_discodata_update",
    CAST("Percentage_assessment_Bad" AS VARCHAR) AS "Percentage_assessment_Bad",
    CAST("Percentage_assessment_Good" AS VARCHAR) AS "Percentage_assessment_Good",
    CAST("Percentage_assessment_Poor" AS VARCHAR) AS "Percentage_assessment_Poor",
    CAST("Percentage_assessment_Unknown" AS VARCHAR) AS "Percentage_assessment_Unknown"
FROM "european-environment-agency-bise.conservation-status-habitats-art17"
