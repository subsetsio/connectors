-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Product" AS "product",
    "Place" AS "place",
    "or era" AS "or_era",
    "local units" AS "local_units",
    "kg./liter" AS "kg_liter",
    "c5",
    "Source" AS "source",
    "c7",
    "Corn - ear, husked" AS "corn_ear_husked",
    "bushel",
    "35.239" AS "35_239",
    "70",
    "31.7513" AS "31_7513",
    "0.9010272709214223" AS "0_9010272709214223",
    "(Maize)" AS "maize"
FROM "gpih-weight-vs-volume"
