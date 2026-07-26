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
    "STATEFP" AS statefp,
    "GEOID" AS geoid,
    "LOGRADE" AS lograde,
    "HIGRADE" AS higrade,
    "GEO_YEAR" AS geo_year,
    "SCHOOLYEAR" AS schoolyear,
    "Shape_Length" AS shape_length,
    "Shape_Area" AS shape_area,
    "OBJECTID" AS objectid,
    "ELSDLEA" AS elsdlea,
    "SCSDLEA" AS scsdlea,
    "UNSDLEA" AS unsdlea,
    "NAME" AS name,
    "LSAD" AS lsad,
    "MTFCC" AS mtfcc,
    "SDTYP" AS sdtyp,
    "FUNCSTAT" AS funcstat,
    "ALAND" AS aland,
    "AWATER" AS awater,
    "INTPTLAT" AS intptlat,
    "INTPTLON" AS intptlon
FROM "u-s-department-of-education-school-district-composites-sy-2020-21-tl-21-a49cb"
