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
    "Archived Informaiton" AS archived_informaiton,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Archived Information" AS archived_information,
    "Archived Informaton" AS archived_informaton,
    "Fiscal Year 2003 Title I Grants to Local Educational Agencies - MISSOURI" AS fiscal_year_2003_title_i_grants_to_local_educational_agencies_missouri,
    "Unnamed: 3" AS unnamed_3,
    "Fiscal Year 2003 Title I Grants to Local Educational Agencies - PENNSYLVANIA" AS fiscal_year_2003_title_i_grants_to_local_educational_agencies_pennsylvania
FROM "u-s-department-of-education-esea-title-i-lea-allocations-fy-2003-5c71e"
