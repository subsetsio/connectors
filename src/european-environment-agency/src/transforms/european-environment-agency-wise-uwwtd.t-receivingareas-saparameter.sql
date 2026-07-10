SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("rcaCDateOtherDirective" AS VARCHAR) AS "rcaCDateOtherDirective",
    CAST("rcaCDateOtherDirective_original" AS VARCHAR) AS "rcaCDateOtherDirective_original",
    CAST("rcaCIDOtherDirective" AS VARCHAR) AS "rcaCIDOtherDirective",
    CAST("rcaCode" AS VARCHAR) AS "rcaCode",
    CAST("rcaCRelevantDirective" AS VARCHAR) AS "rcaCRelevantDirective",
    CAST("rcaDateDesignation" AS VARCHAR) AS "rcaDateDesignation",
    CAST("rcaDateDesignation_original" AS VARCHAR) AS "rcaDateDesignation_original",
    CAST("rcaParameter" AS VARCHAR) AS "rcaParameter",
    CAST("rcaStartDate" AS VARCHAR) AS "rcaStartDate",
    CAST("rcaStartDate_original" AS VARCHAR) AS "rcaStartDate_original",
    CAST("ReceivingAreas_SAParametersId" AS VARCHAR) AS "ReceivingAreas_SAParametersId",
    CAST("repCode" AS VARCHAR) AS "repCode"
FROM "european-environment-agency-wise-uwwtd.t-receivingareas-saparameter"
