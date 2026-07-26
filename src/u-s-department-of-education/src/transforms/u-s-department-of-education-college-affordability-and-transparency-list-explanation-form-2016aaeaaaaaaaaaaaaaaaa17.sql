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
    "College Affordability and Transparency Data Files, 2014" AS college_affordability_and_transparency_data_files_2014,
    "Unnamed: 1" AS unnamed_1,
    "Sector" AS sector,
    "Sector name" AS sector_name,
    "UnitID" AS unitid,
    "OPEID" AS opeid,
    "Name of institution" AS name_of_institution,
    "State" AS state,
    "2014-15 Tuition and fees" AS 2014_15_tuition_and_fees,
    "List A: High tuition and fee indicator" AS list_a_high_tuition_and_fee_indicator,
    "List E: Low tuition and fee indicator" AS list_e_low_tuition_and_fee_indicator,
    "2013-14 Net price" AS 2013_14_net_price,
    "Percent receiving grant aid 2013-13" AS percent_receiving_grant_aid_2013_13,
    "List B: High net price indicator" AS list_b_high_net_price_indicator,
    "List F: Low net price indicator" AS list_f_low_net_price_indicator,
    "Calendar system" AS calendar_system,
    "2012-13 Tuition and fees" AS 2012_13_tuition_and_fees,
    "Percent change" AS percent_change,
    "List C: High percent change tuition and fee indicator" AS list_c_high_percent_change_tuition_and_fee_indicator,
    "2011-12 Net price" AS 2011_12_net_price,
    "List D: High percent change net price indicator" AS list_d_high_percent_change_net_price_indicator
FROM "u-s-department-of-education-college-affordability-and-transparency-list-explanation-form-2016aaeaaaaaaaaaaaaaaaa17"
