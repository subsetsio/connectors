-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SourceGlobalID" AS sourceglobalid,
    "SourceOID" AS sourceoid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "MapMethod" AS mapmethod,
    "Comments" AS comments,
    "GISAcres" AS gisacres,
    "DeleteThis" AS deletethis,
    "Label" AS label,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "PolygonDateTime" AS polygondatetime,
    "IRWINID" AS irwinid,
    "CpxName" AS cpxname,
    "GISS_Misc" AS giss_misc,
    "GISS_Misc2" AS giss_misc2,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-5c5cdca154e84eb39b022a6b9ebb31ff-7"
