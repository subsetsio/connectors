-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "row_number",
    "OBJECTID" AS objectid,
    "STATEFP" AS statefp,
    "ELSDLEA" AS elsdlea,
    "SCSDLEA" AS scsdlea,
    "UNSDLEA" AS unsdlea,
    "SDADMLEA" AS sdadmlea,
    "GEOID" AS geoid,
    "NAME" AS name,
    "LSAD" AS lsad,
    "LOGRADE" AS lograde,
    "HIGRADE" AS higrade,
    "MTFCC" AS mtfcc,
    "SDTYP" AS sdtyp,
    "FUNCSTAT" AS funcstat,
    "ALAND" AS aland,
    "AWATER" AS awater,
    "INTPTLAT" AS intptlat,
    "INTPTLON" AS intptlon,
    "GEO_YEAR" AS geo_year,
    "SCHOOLYEAR" AS schoolyear,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "u-s-department-of-education-school-district-boundaries-current"
