-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "year",
    "month",
    "$/cord" AS "cord",
    "$/(unit)" AS "unit",
    "Type (unit)" AS "type_unit",
    "£/cord" AS "cord_2",
    "£/cord_2" AS "cord_2_2",
    "s/cord" AS "s_cord",
    "d/cord" AS "d_cord",
    "Notes" AS "notes",
    "Source" AS "source",
    "c11",
    "c12",
    "Cords" AS "cords",
    "$/Unit" AS "unit_2",
    "Location" AS "location"
FROM "gpih-firewood-prices-assorted-places-1741-1840-philadelphia-1841-1965"
