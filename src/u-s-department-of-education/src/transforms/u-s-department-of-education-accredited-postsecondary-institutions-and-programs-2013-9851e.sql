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
    "sheet_name",
    "row_number",
    "Institution_ID" AS institution_id,
    "Institution_Name" AS institution_name,
    "Institution_Address" AS institution_address,
    "Institution_City" AS institution_city,
    "Institution_State" AS institution_state,
    "Institution_Zip" AS institution_zip,
    "Institution_Phone" AS institution_phone,
    "Institution_OPEID" AS institution_opeid,
    "Institution_IPEDS_UnitID" AS institution_ipeds_unitid,
    "Institution_Web_Address" AS institution_web_address,
    "Campus_ID" AS campus_id,
    "Campus_Name" AS campus_name,
    "Campus_Address" AS campus_address,
    "Campus_City" AS campus_city,
    "Campus_State" AS campus_state,
    "Campus_Zip" AS campus_zip,
    "Campus_IPEDS_UnitID" AS campus_ipeds_unitid,
    "Accreditation_Type" AS accreditation_type,
    "Agency_Name" AS agency_name,
    "Agency_Status" AS agency_status,
    "Program_Name" AS program_name,
    "Accreditation_Status" AS accreditation_status,
    "Accreditation_Date_Type" AS accreditation_date_type,
    "Periods" AS periods,
    "Last Action" AS last_action
FROM "u-s-department-of-education-accredited-postsecondary-institutions-and-programs-2013-9851e"
