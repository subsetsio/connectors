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
    "Unnamed: 0" AS unnamed_0,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Archived Information" AS archived_information,
    "Unnamed: 4" AS unnamed_4,
    "Archived Informaton" AS archived_informaton,
    "Fiscal Year 2004 Title I Grants to Local Educational Agencies - OKLAHOMA" AS fiscal_year_2004_title_i_grants_to_local_educational_agencies_oklahoma,
    "Unnamed: 3" AS unnamed_3,
    "Archived Informaiton" AS archived_informaiton,
    "Fiscal Year 2004 Title I Grants to Local Educational Agencies - TENNESSEE" AS fiscal_year_2004_title_i_grants_to_local_educational_agencies_tennessee,
    "Fiscal Year 2004 Title I Grants to Local Educational Agencies - VIRGINIA" AS fiscal_year_2004_title_i_grants_to_local_educational_agencies_virginia
FROM "u-s-department-of-education-esea-title-i-lea-allocations-fy-2004-f1c81"
