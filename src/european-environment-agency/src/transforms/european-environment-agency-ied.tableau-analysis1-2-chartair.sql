SELECT
    CAST("Accidental amount released" AS VARCHAR) AS "Accidental amount released",
    CAST("Activity" AS VARCHAR) AS "Activity",
    CAST("Address" AS VARCHAR) AS "Address",
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("Facility" AS VARCHAR) AS "Facility",
    CAST("FacilityId" AS VARCHAR) AS "FacilityId",
    CAST("Pollutant group" AS VARCHAR) AS "Pollutant group",
    CAST("Pollutant Name" AS VARCHAR) AS "Pollutant Name",
    CAST("Postal Code" AS VARCHAR) AS "Postal Code",
    CAST("ReleaseTarget" AS VARCHAR) AS "ReleaseTarget",
    CAST("Total amount released" AS VARCHAR) AS "Total amount released",
    CAST("Town/Village" AS VARCHAR) AS "Town/Village"
FROM "european-environment-agency-ied.tableau-analysis1-2-chartair"
