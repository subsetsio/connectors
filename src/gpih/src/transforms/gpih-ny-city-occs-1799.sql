-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "ID" AS id,
    "Last Name" AS last_name,
    "First Name" AS first_name,
    "Occupation" AS occupation,
    "code",
    "c5",
    "c6",
    "c7"
FROM "gpih-ny-city-occs-1799"
