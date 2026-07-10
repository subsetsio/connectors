SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("eprtrAuthLastUpdated" AS VARCHAR) AS "eprtrAuthLastUpdated",
    CAST("eprtrReportingDate" AS VARCHAR) AS "eprtrReportingDate",
    CAST("eprtrReportingYear" AS VARCHAR) AS "eprtrReportingYear",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("facilityAddress" AS VARCHAR) AS "facilityAddress",
    CAST("facilityContactMail" AS VARCHAR) AS "facilityContactMail",
    CAST("facilityContactPerson" AS VARCHAR) AS "facilityContactPerson",
    CAST("facilityIndustrialActivity" AS VARCHAR) AS "facilityIndustrialActivity",
    CAST("facilityInspireId" AS VARCHAR) AS "facilityInspireId",
    CAST("facilityMainActivity" AS VARCHAR) AS "facilityMainActivity",
    CAST("facilityName" AS VARCHAR) AS "facilityName",
    CAST("facilityNameInspireID" AS VARCHAR) AS "facilityNameInspireID",
    CAST("facilityOrganizationName" AS VARCHAR) AS "facilityOrganizationName",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName"
FROM "european-environment-agency-ied.browse7header"
