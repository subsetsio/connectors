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
    "SrcName" AS srcname,
    "ncessch",
    "schnam",
    "leaid",
    "gslo",
    "gshi",
    "defacto",
    "stAbbrev" AS stabbrev,
    "openEnroll" AS openenroll,
    "level",
    "MultiBdy" AS multibdy,
    "Shape_Length" AS shape_length,
    "Shape_Area" AS shape_area,
    "OBJECTID" AS objectid,
    "Shape_Leng" AS shape_leng
FROM "u-s-department-of-education-school-attendance-boundary-survey-2015-2016-dee8f"
