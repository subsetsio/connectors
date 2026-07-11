-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "LineID" AS lineid,
    "PODSteward" AS podsteward,
    "UniqueID" AS uniqueid,
    "GeoArea" AS geoarea,
    "GISMiles" AS gismiles,
    "IsVisible" AS isvisible,
    "FeatureAccess" AS featureaccess,
    "LineName" AS linename,
    "Label" AS label,
    "LineType" AS linetype,
    "LineStatus" AS linestatus,
    "VersionDate" AS versiondate,
    "GlobalID" AS globalid
FROM "nifc-cc50b6ca69734e4180d5399006058e58-0"
