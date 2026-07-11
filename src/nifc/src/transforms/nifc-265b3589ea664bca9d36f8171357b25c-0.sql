-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GeometryID" AS geometryid,
    "JurisdictionalUnitID" AS jurisdictionalunitid,
    "JurisdictionalUnitID_sansUS" AS jurisdictionalunitid_sansus,
    "JurisdictionalUnitName" AS jurisdictionalunitname,
    "LocalName" AS localname,
    "JurisdictionalKind" AS jurisdictionalkind,
    "JurisdictionalCategory" AS jurisdictionalcategory,
    "LandownerKind" AS landownerkind,
    "LandownerCategory" AS landownercategory,
    "LandownerDepartment" AS landownerdepartment,
    "Comments" AS comments,
    "DataSource" AS datasource,
    "SecondaryDataSource" AS secondarydatasource,
    "SourceUniqueID" AS sourceuniqueid,
    "JoinMethod" AS joinmethod,
    "GISSourceDate" AS gissourcedate,
    "ImportDate" AS importdate,
    "RevisionDate" AS revisiondate,
    "GlobalID" AS globalid,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-265b3589ea664bca9d36f8171357b25c-0"
