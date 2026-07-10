SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_observationStatus" AS VARCHAR) AS "metadata_observationStatus",
    CAST("metadata_statements" AS VARCHAR) AS "metadata_statements",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("monitoringSiteIdentifier" AS VARCHAR) AS "monitoringSiteIdentifier",
    CAST("monitoringSiteIdentifierScheme" AS VARCHAR) AS "monitoringSiteIdentifierScheme",
    CAST("observedPropertyDeterminandCode" AS VARCHAR) AS "observedPropertyDeterminandCode",
    CAST("observedPropertyDeterminandLabel" AS VARCHAR) AS "observedPropertyDeterminandLabel",
    CAST("phenomenonTimeReferenceYear" AS VARCHAR) AS "phenomenonTimeReferenceYear",
    CAST("procedureEstimateDetail" AS VARCHAR) AS "procedureEstimateDetail",
    CAST("Remarks" AS VARCHAR) AS "Remarks",
    CAST("resultEmissionsUom" AS VARCHAR) AS "resultEmissionsUom",
    CAST("resultEmissionsValue" AS VARCHAR) AS "resultEmissionsValue",
    CAST("resultObservationStatus" AS VARCHAR) AS "resultObservationStatus",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-soe.waterbase-t-wise1-riverineinputloads"
