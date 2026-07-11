-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "OBJECTID" AS objectid,
    "CLC" AS clc,
    "FEATURE_ID_1" AS feature_id_1,
    "NAME" AS name,
    "NOM" AS nom,
    "PERIM_KM" AS perim_km,
    "AREA_KM2" AS area_km2,
    "LAT_DD" AS lat_dd,
    "LON_DD" AS lon_dd,
    "KIND" AS kind,
    "USAGE" AS usage,
    "DEPICTN" AS depictn,
    "PROVINCE_C" AS province_c,
    "COUNTRY_C" AS country_c,
    "WATRBODY_C" AS watrbody_c,
    "Shape_Leng" AS shape_leng,
    "Shape_Le_1" AS shape_le_1,
    "Shape_Area" AS shape_area,
    "version",
    "geometry_type",
    "geometry_json"
FROM "environment-and-climate-change-canada-public-standard-forecast-zones"
