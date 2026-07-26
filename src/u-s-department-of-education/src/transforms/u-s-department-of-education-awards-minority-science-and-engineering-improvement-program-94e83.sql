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
    "FY 2019 MINORITY SCIENCE AND ENGINEERING IMPROVEMENT PROGRAM NEW AWARDS" AS fy_2019_minority_science_and_engineering_improvement_program_new_awards,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "FY 2019 Minority Science and Engineering Improvement Program Noncompeting Continuation Awards (NCCs)" AS fy_2019_minority_science_and_engineering_improvement_program_noncompeting_continuation_awards_nccs,
    "Attachment 2: Fiscal Year 2017 Minority Science and Engineering Improvement Program Supplemental Award" AS attachment_2_fiscal_year_2017_minority_science_and_engineering_improvement_program_supplemental_award,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10,
    "Unnamed: 11" AS unnamed_11,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 0" AS unnamed_0,
    "FY 2018 MINORITY SCIENCE AND ENGINEERING IMPROVEMENT PROGRAM NEW AWARDS" AS fy_2018_minority_science_and_engineering_improvement_program_new_awards,
    "FY 2018 MINORITY SCIENCE AND ENGINEERING IMPROVEMENT PROGRAM NONCOMPETING CONTINUATION AWARDS (NCCs)" AS fy_2018_minority_science_and_engineering_improvement_program_noncompeting_continuation_awards_nccs,
    "FY 2017 MINORITY SCIENCE AND ENGINEERING IMPROVEMENT PROGRAM NEW AWARDS" AS fy_2017_minority_science_and_engineering_improvement_program_new_awards,
    "FY 2017 MINORITY SCIENCE AND ENGINEERING IMPROVEMENT PROGRAM NONCOMPETING CONTINUATION AWARDS (NCCS)" AS fy_2017_minority_science_and_engineering_improvement_program_noncompeting_continuation_awards_nccs,
    "FY 2016 Minority Science and Engineering Improvement Program" AS fy_2016_minority_science_and_engineering_improvement_program,
    "FY 2015 Minority Science and Engineering Improvement Program" AS fy_2015_minority_science_and_engineering_improvement_program,
    "PR NUMBER" AS pr_number,
    "MSEIP GRANTEE NAME" AS mseip_grantee_name,
    "STATE" AS state,
    "FY 2011 Awards" AS fy_2011_awards
FROM "u-s-department-of-education-awards-minority-science-and-engineering-improvement-program-94e83"
