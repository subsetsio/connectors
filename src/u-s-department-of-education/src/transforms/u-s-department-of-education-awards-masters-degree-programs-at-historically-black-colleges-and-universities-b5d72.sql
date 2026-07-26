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
    "PR Number" AS pr_number,
    "State" AS state,
    "Master's Degree Programs at Historically Black Colleges and Universities FY 2011 Grantees (Non-Competing Continuation)" AS master_s_degree_programs_at_historically_black_colleges_and_universities_fy_2011_grantees_non_competing_continuation,
    "FY 2011 Awards" AS fy_2011_awards,
    "HBCU Master's Grantee" AS hbcu_master_s_grantee,
    "FY 2010 Awards" AS fy_2010_awards,
    "FY 2009 Awards" AS fy_2009_awards
FROM "u-s-department-of-education-awards-masters-degree-programs-at-historically-black-colleges-and-universities-b5d72"
