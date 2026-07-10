SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_observationStatus" AS VARCHAR) AS "metadata_observationStatus",
    CAST("metadata_statements" AS VARCHAR) AS "metadata_statements",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("monitoringSiteIdentifier" AS VARCHAR) AS "monitoringSiteIdentifier",
    CAST("monitoringSiteIdentifierScheme" AS VARCHAR) AS "monitoringSiteIdentifierScheme",
    CAST("observedProperty" AS VARCHAR) AS "observedProperty",
    CAST("phenomenonTimePeriod" AS VARCHAR) AS "phenomenonTimePeriod",
    CAST("phenomenonTimePeriod_day" AS VARCHAR) AS "phenomenonTimePeriod_day",
    CAST("phenomenonTimePeriod_month" AS VARCHAR) AS "phenomenonTimePeriod_month",
    CAST("phenomenonTimePeriod_year" AS VARCHAR) AS "phenomenonTimePeriod_year",
    CAST("Remarks" AS VARCHAR) AS "Remarks",
    CAST("resultObservationStatus" AS VARCHAR) AS "resultObservationStatus",
    CAST("resultObservedValue" AS VARCHAR) AS "resultObservedValue",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-soe.waterbase-t-wise3-monitoringdata"
