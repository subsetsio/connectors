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
    "£" AS "column",
    "s",
    "d",
    "physical unit" AS "physical_unit",
    "£/cord" AS "cord",
    "Service" AS "service",
    "Source: https://jerseyhistory.org/archives-browse-colonial-p" AS "source_https_jerseyhistory_org_archives_browse_colonial_p"
FROM "gpih-firewood-prices-new-jersey-1757-1791"
