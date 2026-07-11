-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "row",
    "Region" AS "region",
    "Nation" AS "nation",
    "Place" AS "place",
    "Classes" AS "classes",
    "Years" AS "years",
    "year",
    "male",
    "female",
    "both",
    "both_2",
    "rate (%)" AS "rate",
    "Source" AS "source"
FROM "gpih-life-exp-infant-mort"
