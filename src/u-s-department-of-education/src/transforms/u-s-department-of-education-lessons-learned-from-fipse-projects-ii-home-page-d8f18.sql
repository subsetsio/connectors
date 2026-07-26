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
    "archive_member",
    "row_number",
    "_Lessons Learned from FIPSE Projects II - September 1993_" AS lessons_learned_from_fipse_projects_ii_september_1993,
    "Lessons Learned" AS lessons_learned,
    "_subsets_record_type" AS subsets_record_type,
    "error"
FROM "u-s-department-of-education-lessons-learned-from-fipse-projects-ii-home-page-d8f18"
