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
    "LOCALE" AS locale,
    "STATEFP" AS statefp,
    "Shape_Length" AS shape_length,
    "Shape_Area" AS shape_area,
    "GEO_YEAR" AS geo_year,
    "_subsets_record_type" AS subsets_record_type,
    "error"
FROM "u-s-department-of-education-locales-2019"
