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
    "[Code of Federal Regulations]" AS code_of_federal_regulations,
    "sheet_name",
    "FISCAL YEAR ALLOCATIONS FOR GRANTS TO STATES INDIVIDUALS WITH DISABILITIES EDUCATION ACT - PART B, SECTION 611 - TABLE I" AS fiscal_year_allocations_for_grants_to_states_individuals_with_disabilities_education_act_part_b_section_611_table_i,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "FISCAL YEAR ALLOCATIONS FOR PRESCHOOL GRANTS INDIVIDUALS WITH DISABILITIES EDUCATION ACT - PART B, SECTION 619 - TABLE II APRIL 30, 2012" AS fiscal_year_allocations_for_preschool_grants_individuals_with_disabilities_education_act_part_b_section_619_table_ii_april_30_2012,
    "FISCAL YEAR 2012 ALLOCATIONS FOR THE GRANTS FOR INFANTS AND FAMILIES PROGRAM INDIVIDUALS WITH DISABILITIES EDUCATION ACT - PART C (April 30, 2012)" AS fiscal_year_2012_allocations_for_the_grants_for_infants_and_families_program_individuals_with_disabilities_education_act_part_c_april_30_2012
FROM "u-s-department-of-education-2012-parts-b-and-c-formula-grant-funding-tables"
