SELECT
    CAST("Contact" AS VARCHAR) AS "Contact",
    CAST("Cooperation_Experience" AS VARCHAR) AS "Cooperation_Experience",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("General_Information" AS VARCHAR) AS "General_Information",
    CAST("Legal_Policies" AS VARCHAR) AS "Legal_Policies",
    CAST("Monitoring_Evaluation" AS VARCHAR) AS "Monitoring_Evaluation",
    CAST("National_Circumstances" AS VARCHAR) AS "National_Circumstances",
    CAST("Strategies_Plans" AS VARCHAR) AS "Strategies_Plans"
FROM "european-environment-agency-nccaps.adaptation-json"
