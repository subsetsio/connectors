SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("rcaCode" AS VARCHAR) AS "rcaCode",
    CAST("rcaCodePredecessor" AS VARCHAR) AS "rcaCodePredecessor",
    CAST("rcaEvolutionType" AS VARCHAR) AS "rcaEvolutionType",
    CAST("rcasalsaRemark" AS VARCHAR) AS "rcasalsaRemark",
    CAST("ReceivingAreas_SALSApredecessorID" AS VARCHAR) AS "ReceivingAreas_SALSApredecessorID",
    CAST("repCode" AS VARCHAR) AS "repCode"
FROM "european-environment-agency-wise-uwwtd.t-receivingareas-salsapredecessor"
