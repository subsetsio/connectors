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
    "Source(s): Richmond Dispatch, Richmond Times-Dispatch" AS "source_s_richmond_dispatch_richmond_times_dispatch",
    "c4",
    "c5",
    "Type" AS "type",
    "Notes" AS "notes",
    "Source" AS "source",
    "Type (unit)" AS "type_unit",
    "$/(half-cord)" AS "half_cord",
    "c7",
    "$/(unit)" AS "unit"
FROM "gpih-firewood-prices-richmond-va-1852-1967"
