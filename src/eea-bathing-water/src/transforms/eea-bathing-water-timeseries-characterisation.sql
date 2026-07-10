-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Characterisation rows are versioned reported observations; metadata lifecycle fields identify revisions and should be considered when selecting current versus historical records.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "geographicalConstraint" AS geographicalconstraint,
    "groupIdentifier" AS groupidentifier,
    "link",
    CAST("metadata_beginLifeSpanVersion" AS TIMESTAMP) AS metadata_beginlifespanversion,
    "metadata_endLifeSpanVersion" AS metadata_endlifespanversion,
    "metadata_observationStatus" AS metadata_observationstatus,
    "metadata_replacedBy" AS metadata_replacedby,
    "metadata_replaces",
    "metadata_statements",
    "metadata_statusCode" AS metadata_statuscode,
    CAST("metadata_statusDate" AS TIMESTAMP) AS metadata_statusdate,
    "metadata_versionId" AS metadata_versionid,
    "qualityClass" AS qualityclass,
    "remarks",
    "season",
    "UID" AS uid
FROM "eea-bathing-water-timeseries-characterisation"
