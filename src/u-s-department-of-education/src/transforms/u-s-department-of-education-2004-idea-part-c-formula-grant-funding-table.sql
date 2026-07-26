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
    "Grants for Infants and Families Program (Part C) - FY 2004 Allocations" AS grants_for_infants_and_families_program_part_c_fy_2004_allocations,
    "Unnamed: 1" AS unnamed_1
FROM "u-s-department-of-education-2004-idea-part-c-formula-grant-funding-table"
