-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
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
    "ComplexName" AS complexname,
    "ComplexID" AS complexid,
    "GACC" AS gacc,
    "IMTName" AS imtname,
    "UnitID" AS unitid,
    "LocalIncidentID" AS localincidentid,
    "IRWINID" AS irwinid,
    "GeometryID" AS geometryid,
    "GlobalID" AS globalid,
    "OBJECTID" AS objectid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    CAST("ORIGINAL_OBJECTID" AS BIGINT) AS original_objectid,
    "SHAPE__Area" AS shape_area,
    "SHAPE__Length" AS shape_length
FROM "nifc-2827d083ddc14464a8eab3181e8bf13e-2"
