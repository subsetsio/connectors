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
    "Fines Imposed by Federal Student Aid" AS fines_imposed_by_federal_student_aid,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "This tab provides definitions for Fines Imposed by Federal Student Aid" AS this_tab_provides_definitions_for_fines_imposed_by_federal_student_aid,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2010" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2010,
    "Unnamed: 7" AS unnamed_7,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2011" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2011,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2012" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2012,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2013" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2013,
    "OPEID" AS opeid,
    "SCH_NAME" AS sch_name,
    "CTY_NAME" AS cty_name,
    "ST_CD" AS st_cd,
    "SCH_TYPE" AS sch_type,
    "REASON_REFER_DESC" AS reason_refer_desc,
    "IMPOSED_FINE_AMT" AS imposed_fine_amt,
    "OUTCOME_DT" AS outcome_dt,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2015" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2015,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2016" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2016,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2017" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2017,
    "Fines Imposed by Federal Student Aid in Fiscal Year 2018" AS fines_imposed_by_federal_student_aid_in_fiscal_year_2018,
    "Fines Imposed by Federal Student Aid in FY 2019" AS fines_imposed_by_federal_student_aid_in_fy_2019
FROM "u-s-department-of-education-school-data"
