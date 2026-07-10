SELECT
    CAST("AdministrativeLevelMeasureImplemented" AS VARCHAR) AS "AdministrativeLevelMeasureImplemented",
    CAST("AdministrativeOther" AS VARCHAR) AS "AdministrativeOther",
    CAST("ClimateThreat" AS VARCHAR) AS "ClimateThreat",
    CAST("costImplementingMeasure" AS VARCHAR) AS "costImplementingMeasure",
    CAST("Examples" AS VARCHAR) AS "Examples",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("KeyTypeMeasure" AS VARCHAR) AS "KeyTypeMeasure",
    CAST("ReportNet3HistoricReleaseId" AS VARCHAR) AS "ReportNet3HistoricReleaseId",
    CAST("SectorsAffected" AS VARCHAR) AS "SectorsAffected",
    CAST("shortDescriptionMeasureAction" AS VARCHAR) AS "shortDescriptionMeasureAction",
    CAST("specification" AS VARCHAR) AS "specification",
    CAST("Status" AS VARCHAR) AS "Status",
    CAST("subKTM" AS VARCHAR) AS "subKTM",
    CAST("Title" AS VARCHAR) AS "Title"
FROM "european-environment-agency-nccaps.actionmeasureswithcodelistvalues"
