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
    "Title IV Institutions Reporting Cash Management Contracts" AS title_iv_institutions_reporting_cash_management_contracts,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "This tab provides definitions of those terms in the Title IV Institutions Reporting Cash Management Contracts report." AS this_tab_provides_definitions_of_those_terms_in_the_title_iv_institutions_reporting_cash_management_contracts_report
FROM "u-s-department-of-education-cash-management-contracts"
