-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "c0",
    "Q1" AS q1,
    "Q2" AS q2,
    "Q3" AS q3,
    "Q4" AS q4,
    "Average" AS average,
    "Q1_2" AS q1_2,
    "Q2_2" AS q2_2,
    "Q3_2" AS q3_2,
    "Q4_2" AS q4_2,
    "Average_2" AS average_2,
    "Q1_3" AS q1_3,
    "Q2_3" AS q2_3,
    "Q3_3" AS q3_3,
    "Q4_3" AS q4_3,
    "Average_3" AS average_3,
    "gAg/year" AS gag_year,
    "gAg/year_2" AS gag_year_2,
    "gAg/year_3" AS gag_year_3,
    "c19",
    "(140-143)" AS 140_143,
    "31-32):" AS 31_32,
    "grosz",
    "per ___?" AS per,
    "Nombre des" AS nombre_des,
    "Taux moyen" AS taux_moyen
FROM "gpih-lviv-wages-int-1500-1700"
