-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Seasonal-period rows include period types and revision metadata; use periodType and lifecycle fields when comparing bathing-season dates across reports.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    strptime("endDate", '%Y-%m-%d')::DATE AS enddate,
    "managementMeasures" AS managementmeasures,
    CAST("metadata_beginLifeSpanVersion" AS TIMESTAMP) AS metadata_beginlifespanversion,
    "metadata_endLifeSpanVersion" AS metadata_endlifespanversion,
    "metadata_observationStatus" AS metadata_observationstatus,
    "metadata_replacedBy" AS metadata_replacedby,
    "metadata_replaces",
    "metadata_statements",
    "metadata_statusCode" AS metadata_statuscode,
    CAST("metadata_statusDate" AS TIMESTAMP) AS metadata_statusdate,
    "metadata_versionId" AS metadata_versionid,
    "periodType" AS periodtype,
    "remarks",
    "season",
    strptime("startDate", '%Y-%m-%d')::DATE AS startdate,
    "UID" AS uid
FROM "eea-bathing-water-timeseries-seasonalperiod"
