-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "States" AS states,
    "c1",
    "No. of Acres" AS no_of_acres,
    "Valuation" AS valuation,
    "Number" AS number,
    "Valuation_2" AS valuation_2,
    "1800 census" AS 1800_census,
    "Numbers" AS numbers,
    "1800 census_2" AS 1800_census_2,
    "Lands" AS lands,
    "Dwelling-houses" AS dwelling_houses,
    "Slaves" AS slaves,
    "Total" AS total,
    "$/acre" AS acre,
    "$/dwelling" AS dwelling,
    "land",
    "dwellings",
    "slave 12-50" AS slave_12_50
FROM "gpih-pitkin-summary-1798-tax-b"
