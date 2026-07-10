SELECT
    CAST("Contact" AS VARCHAR) AS "Contact",
    CAST("Cooperation_Experience" AS VARCHAR) AS "Cooperation_Experience",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("General_Information" AS VARCHAR) AS "General_Information",
    CAST("Key_Affected_Sectors" AS VARCHAR) AS "Key_Affected_Sectors",
    CAST("Legal_Policies" AS VARCHAR) AS "Legal_Policies",
    CAST("Monitoring_Evaluation" AS VARCHAR) AS "Monitoring_Evaluation",
    CAST("National_Circumstances" AS VARCHAR) AS "National_Circumstances",
    CAST("Observed_Future_Climate_Hazards" AS VARCHAR) AS "Observed_Future_Climate_Hazards",
    CAST("ReportNet3HistoricReleaseId" AS VARCHAR) AS "ReportNet3HistoricReleaseId",
    CAST("Strategies_Plans" AS VARCHAR) AS "Strategies_Plans",
    CAST("Sub_National_Adaptation" AS VARCHAR) AS "Sub_National_Adaptation"
FROM "european-environment-agency-nccaps.ec-adaptation-art19-json-2025"
