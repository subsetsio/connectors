-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Occupation" AS occupation,
    "Count" AS count,
    "Orig. row" AS orig_row,
    "Last Name" AS last_name,
    "First Name" AS first_name,
    "Male" AS male,
    "Female" AS female,
    "c6"
FROM "gpih-charleston-city-directory-1800"
