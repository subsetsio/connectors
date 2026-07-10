SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("eprtrActivityCode" AS VARCHAR) AS "eprtrActivityCode",
    CAST("eprtrActivityName" AS VARCHAR) AS "eprtrActivityName",
    CAST("eprtrSectorName" AS VARCHAR) AS "eprtrSectorName",
    CAST("reportingYear" AS VARCHAR) AS "reportingYear",
    CAST("WasteClassification" AS VARCHAR) AS "WasteClassification",
    CAST("WasteTransfer" AS VARCHAR) AS "WasteTransfer",
    CAST("WasteTreatement" AS VARCHAR) AS "WasteTreatement"
FROM "european-environment-agency-ied.tableau-analysis-wastesector-trend"
