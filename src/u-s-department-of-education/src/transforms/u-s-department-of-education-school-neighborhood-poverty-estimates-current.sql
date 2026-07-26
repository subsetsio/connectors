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
    "School ID" AS school_id,
    "Name" AS name,
    "IPR_EST" AS ipr_est,
    "IPR_SE" AS ipr_se,
    "LAT" AS lat,
    "LON" AS lon,
    "LEAID" AS leaid,
    "School Year" AS school_year,
    "x",
    "y"
FROM "u-s-department-of-education-school-neighborhood-poverty-estimates-current"
