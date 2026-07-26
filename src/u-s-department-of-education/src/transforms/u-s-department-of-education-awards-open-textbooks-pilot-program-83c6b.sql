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
    "FY 2019 OPEN TEXTBOOKS PILOT PROGRAM NEW AWARD" AS fy_2019_open_textbooks_pilot_program_new_award,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "FY 2018 OPEN TEXTBOOKS PILOT PROGRAM NEW AWARD" AS fy_2018_open_textbooks_pilot_program_new_award
FROM "u-s-department-of-education-awards-open-textbooks-pilot-program-83c6b"
