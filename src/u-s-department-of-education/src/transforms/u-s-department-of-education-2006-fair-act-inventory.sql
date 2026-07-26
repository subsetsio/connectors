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
    "Instructions for compiling commercial and inherently governmental FTE inventories" AS instructions_for_compiling_commercial_and_inherently_governmental_fte_inventories,
    "Seq_No" AS seq_no,
    "Agency_Group" AS agency_group,
    "Agy_Bur" AS agy_bur,
    "Dept_or_Agy_Title" AS dept_or_agy_title,
    "Bureau_Title" AS bureau_title,
    "Tot_CY_FTEs" AS tot_cy_ftes,
    "Dir_CY_FTEs" AS dir_cy_ftes,
    "Reim_CY_FTEs" AS reim_cy_ftes,
    "Fct_Code" AS fct_code,
    "Fct_Code_Text" AS fct_code_text,
    "A C NIELSEN" AS a_c_nielsen
FROM "u-s-department-of-education-2006-fair-act-inventory"
