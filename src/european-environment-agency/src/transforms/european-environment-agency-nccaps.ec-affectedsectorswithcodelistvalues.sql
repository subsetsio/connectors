SELECT
    CAST("DescribeImpactsKeyHazards" AS VARCHAR) AS "DescribeImpactsKeyHazards",
    CAST("DescribeLikelihood" AS VARCHAR) AS "DescribeLikelihood",
    CAST("DescribeRisk" AS VARCHAR) AS "DescribeRisk",
    CAST("DescribeVulnerability" AS VARCHAR) AS "DescribeVulnerability",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("ImpactsKeyHazards" AS VARCHAR) AS "ImpactsKeyHazards",
    CAST("ImpactVariation" AS VARCHAR) AS "ImpactVariation",
    CAST("KeyHazardsLikelihood" AS VARCHAR) AS "KeyHazardsLikelihood",
    CAST("LikehoodVariability" AS VARCHAR) AS "LikehoodVariability",
    CAST("PrimarySector" AS VARCHAR) AS "PrimarySector",
    CAST("ReportNet3HistoricReleaseId" AS VARCHAR) AS "ReportNet3HistoricReleaseId",
    CAST("RiskFutureImpacts" AS VARCHAR) AS "RiskFutureImpacts",
    CAST("RiskVariability" AS VARCHAR) AS "RiskVariability",
    CAST("SectorDescribe" AS VARCHAR) AS "SectorDescribe",
    CAST("SectorTitle" AS VARCHAR) AS "SectorTitle",
    CAST("VulnerabilityVariability" AS VARCHAR) AS "VulnerabilityVariability"
FROM "european-environment-agency-nccaps.ec-affectedsectorswithcodelistvalues"
