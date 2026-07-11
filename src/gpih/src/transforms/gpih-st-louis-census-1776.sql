-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Unknown" AS unknown,
    "428",
    "254",
    "170",
    "4",
    "Unknown_2" AS unknown_2,
    "8",
    "row",
    "Name" AS name,
    "unknown = 2" AS unknown_2_2,
    "Age" AS age,
    "Total" AS total,
    "Probably adult" AS probably_adult,
    "Occupation" AS occupation,
    "Nationality" AS nationality,
    "Notes" AS notes
FROM "gpih-st-louis-census-1776"
