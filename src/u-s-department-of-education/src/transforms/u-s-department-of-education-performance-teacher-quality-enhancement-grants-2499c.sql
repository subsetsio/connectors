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
    "sheet_name",
    "row_number",
    "Teacher Quality Enhancement Program: Grantee Level Analysis (2005-06 Data)" AS teacher_quality_enhancement_program_grantee_level_analysis_2005_06_data,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10,
    "Unnamed: 11" AS unnamed_11,
    "Unnamed: 12" AS unnamed_12,
    "Teacher Quality Enhancement Program (TQE)" AS teacher_quality_enhancement_program_tqe,
    "Unnamed: 0" AS unnamed_0,
    "Teacher Quality Enhancement Program: Grantee-Level Analysis (2006-07) for" AS teacher_quality_enhancement_program_grantee_level_analysis_2006_07_for,
    "Teacher Quality Enhancement Program" AS teacher_quality_enhancement_program
FROM "u-s-department-of-education-performance-teacher-quality-enhancement-grants-2499c"
