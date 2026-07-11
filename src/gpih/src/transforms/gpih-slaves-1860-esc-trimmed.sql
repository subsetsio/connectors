-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "year",
    "datanum",
    "serial",
    "slavenum",
    "weight",
    "stateicp",
    "county",
    "city",
    "sizehold",
    "age",
    "Upper ESC" AS "upper_esc",
    "female=0)" AS "female_0",
    "regional rates" AS "regional_rates",
    "total retained" AS "total_retained",
    "of slaves" AS "of_slaves",
    "color",
    "fugitive",
    "manumit",
    "blind (no=0,yes=1)" AS "blind_no_0_yes_1",
    "deaf (no=0,yes=1)" AS "deaf_no_0_yes_1",
    "idiotic (no=0,yes=1)" AS "idiotic_no_0_yes_1",
    "insane (no=0,yes=1)" AS "insane_no_0_yes_1",
    "noholdrs",
    "nhouses",
    "blank, illeg=0" AS "blank_illeg_0",
    "blank, illeg=1" AS "blank_illeg_1",
    "sh1typeg",
    "sh2typeg",
    "sh1ln",
    "sh1fn",
    "sh2ln",
    "sh2fn"
FROM "gpih-slaves-1860-esc-trimmed"
