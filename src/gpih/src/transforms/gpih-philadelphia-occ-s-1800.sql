-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "count",
    "occ count" AS "occ_count",
    "LW code" AS "lw_code",
    "LW occupational class" AS "lw_occupational_class",
    "Occupation" AS "occupation",
    "c5",
    "Orig. row" AS "orig_row",
    "Last Name" AS "last_name",
    "First Name" AS "first_name",
    "Male" AS "male",
    "Female" AS "female",
    "US census category" AS "us_census_category",
    "c1",
    "Males" AS "males",
    "Females" AS "females",
    "Both" AS "both",
    "Males_2" AS "males_2",
    "Females_2" AS "females_2",
    "Both_2" AS "both_2",
    "Males_3" AS "males_3",
    "Females_3" AS "females_3",
    "Both_3" AS "both_3"
FROM "gpih-philadelphia-occ-s-1800"
