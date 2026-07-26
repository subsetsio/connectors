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
    "ELSDLEA" AS elsdlea,
    "UNSDLEA" AS unsdlea,
    "SCSDLEA" AS scsdlea,
    "Shape_Length" AS shape_length,
    "Shape_Area" AS shape_area,
    "OBJECTID" AS objectid
FROM "u-s-department-of-education-school-district-composites-sy-2015-16-tl-16-629e8"
