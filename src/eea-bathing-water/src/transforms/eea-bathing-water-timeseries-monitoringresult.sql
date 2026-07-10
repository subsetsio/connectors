-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are raw reported monitoring samples and include revision metadata; filter sampleStatus and metadata status fields before using them as final assessed observations.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "escherichiaColiStatus" AS escherichiacolistatus,
    "escherichiaColiValue" AS escherichiacolivalue,
    "intestinalEnterococciStatus" AS intestinalenterococcistatus,
    "intestinalEnterococciValue" AS intestinalenterococcivalue,
    CAST("metadata_beginLifeSpanVersion" AS TIMESTAMP) AS metadata_beginlifespanversion,
    "metadata_endLifeSpanVersion" AS metadata_endlifespanversion,
    "metadata_observationStatus" AS metadata_observationstatus,
    "metadata_replacedBy" AS metadata_replacedby,
    "metadata_replaces",
    "metadata_statements",
    "metadata_statusCode" AS metadata_statuscode,
    CAST("metadata_statusDate" AS TIMESTAMP) AS metadata_statusdate,
    "metadata_versionId" AS metadata_versionid,
    "remarks",
    strptime("sampleDate", '%Y-%m-%d')::DATE AS sampledate,
    "sampleStatus" AS samplestatus,
    "season",
    "UID" AS uid
FROM "eea-bathing-water-timeseries-monitoringresult"
