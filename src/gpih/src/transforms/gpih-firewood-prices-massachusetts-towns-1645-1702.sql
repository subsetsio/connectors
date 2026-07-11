-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "Month" AS "month",
    "Cord" AS "cord",
    "foot",
    "£" AS "column",
    "sh." AS "sh",
    "d." AS "d",
    "£/cord" AS "cord_2",
    "s/cord" AS "s_cord",
    "Source" AS "source",
    "Location" AS "location",
    "Shilling" AS "shilling",
    "Shilling_2" AS "shilling_2",
    "d._2" AS "d_2",
    "Citation: http://salem.lib.virginia.edu/Essex/index.html" AS "citation_http_salem_lib_virginia_edu_essex_index_html",
    "c11",
    "c9"
FROM "gpih-firewood-prices-massachusetts-towns-1645-1702"
