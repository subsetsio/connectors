-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "year",
    "month",
    "$/cord" AS cord,
    "Type (unit)" AS type_unit,
    "$/(unit)" AS unit,
    "Notes" AS notes,
    "Source" AS source,
    "1894",
    "4",
    "4.5" AS 4_5,
    "1",
    "4.5_2" AS 4_5_2,
    "Pine" AS pine,
    "New Orleans Times-Picayune" AS new_orleans_times_picayune,
    "1.65" AS 1_65,
    "2.7272727272727275" AS 2_7272727272727275,
    "$/load" AS load
FROM "gpih-firewood-prices-new-orleans-1838-1950"
