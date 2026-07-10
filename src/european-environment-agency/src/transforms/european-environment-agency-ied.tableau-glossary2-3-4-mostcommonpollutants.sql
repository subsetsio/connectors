SELECT
    CAST("accidental" AS VARCHAR) AS "accidental",
    CAST("Activity Name" AS VARCHAR) AS "Activity Name",
    CAST("Activity" AS VARCHAR) AS "Activity",
    CAST("Air pollutant group" AS VARCHAR) AS "Air pollutant group",
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("Facility Inspire Id" AS VARCHAR) AS "Facility Inspire Id",
    CAST("Label" AS VARCHAR) AS "Label",
    CAST("Medium" AS VARCHAR) AS "Medium",
    CAST("total" AS VARCHAR) AS "total",
    CAST("Water pollutant group" AS VARCHAR) AS "Water pollutant group"
FROM "european-environment-agency-ied.tableau-glossary2-3-4-mostcommonpollutants"
