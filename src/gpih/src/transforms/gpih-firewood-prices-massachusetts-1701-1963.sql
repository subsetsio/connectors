-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "year",
    "unit",
    "£" AS column,
    "s",
    "d",
    "$" AS column_2,
    "Old tenor Adjust" AS old_tenor_adjust,
    "£_2" AS 2,
    "c8",
    "dollar/cord" AS dollar_cord,
    "pound/cord" AS pound_cord,
    "year_2",
    "c12",
    "1851",
    "4.09" AS 4_09,
    "5",
    "6",
    "7",
    "c5",
    "7.5" AS 7_5,
    "5.918" AS 5_918,
    "Massachusetts. Report on the Statistics of Labor. Boston. 19" AS massachusetts_report_on_the_statistics_of_labor_boston_19,
    "p. 504" AS p_504,
    "Mass" AS mass,
    "Year_1" AS year_1,
    "Cord (hard)" AS cord_hard,
    "Cord (pine)" AS cord_pine,
    "Dollars" AS dollars,
    "Citation: http://salem.lib.virginia.edu/Essex/index.html" AS citation_http_salem_lib_virginia_edu_essex_index_html,
    "Location" AS location,
    "$/Cord (hard)" AS cord_hard_2,
    "$/Cord (pine)" AS cord_pine_2,
    "Avg ($/cord)" AS avg_cord,
    "Citation: Multiple" AS citation_multiple
FROM "gpih-firewood-prices-massachusetts-1701-1963"
