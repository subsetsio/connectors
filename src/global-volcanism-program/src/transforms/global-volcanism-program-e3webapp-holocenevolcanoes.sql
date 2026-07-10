-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This E3 web-app volcano layer overlaps the canonical Holocene volcanoes catalog and uses a leaner app-facing schema; prefer the Smithsonian_VOTW_Holocene_Volcanoes table for the canonical volcano reference.
SELECT
    "FID" AS fid,
    CAST("VolcanoNumber" AS BIGINT) AS volcanonumber,
    "VolcanoName" AS volcanoname,
    "Country" AS country,
    "Remarks" AS remarks,
    "VolcanoType" AS volcanotype,
    CAST("LastEruption" AS BIGINT) AS lasteruption,
    CAST("Elevation" AS BIGINT) AS elevation,
    "TectonicSetting" AS tectonicsetting,
    CAST("Within_5km" AS BIGINT) AS within_5km,
    CAST("Within_10km" AS BIGINT) AS within_10km,
    CAST("Within_30km" AS BIGINT) AS within_30km,
    CAST("Within_100km" AS BIGINT) AS within_100km,
    "VPImageFileName" AS vpimagefilename,
    "VPImageCaption" AS vpimagecaption,
    "VPImageCredit" AS vpimagecredit,
    CAST("LatitudeDecimal" AS DOUBLE) AS latitudedecimal,
    CAST("LongitudeDecimal" AS DOUBLE) AS longitudedecimal,
    "GeoLocation" AS geolocation
FROM "global-volcanism-program-e3webapp-holocenevolcanoes"
