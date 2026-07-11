-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "District" AS district,
    "Males ≥ 16" AS males_16,
    "Males < 16" AS males_16_2,
    "Females" AS females,
    "free",
    "Slaves" AS slaves,
    "Total" AS total,
    "free_2",
    "c8",
    "Professionals" AS professionals,
    "11 to 19" AS 11_to_19,
    "132",
    "0.09475951184493898" AS 0_09475951184493898,
    "132_2",
    "0.10038022813688213" AS 0_10038022813688213,
    "20",
    "0.091324200913242" AS 0_091324200913242,
    "152",
    "0.09908735332464146" AS 0_09908735332464146,
    "152_2",
    "0.1130952380952381" AS 0_1130952380952381,
    "c0",
    "Last Name" AS last_name,
    "First Name" AS first_name,
    "Occupation" AS occupation,
    "Company (1=yes)" AS company_1_yes,
    "Male" AS male,
    "Female" AS female,
    "c7"
FROM "gpih-charleston-pop-occs-1790-1774"
