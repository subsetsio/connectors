-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "Comments" AS comments,
    "ManagementStrategy" AS managementstrategy,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "Label" AS label,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "LengthFeet" AS lengthfeet,
    "IRWINID" AS irwinid,
    "GISS_Misc" AS giss_misc,
    "GlobalID" AS globalid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "SourceGlobalID" AS sourceglobalid,
    "SourceOID" AS sourceoid,
    "Shape__Length" AS shape_length
FROM "nifc-705b14551df6417aaea99dd7a651d9ff-5"
