-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Commodity" AS "commodity",
    "Beef" AS "beef",
    "Mutton" AS "mutton",
    "Corn" AS "corn",
    "Beef_2" AS "beef_2",
    "Mutton_2" AS "mutton_2",
    "Corn_2" AS "corn_2",
    "Beef_3" AS "beef_3",
    "Mutton_3" AS "mutton_3",
    "Corn_3" AS "corn_3",
    "Soap" AS "soap",
    "Butter" AS "butter",
    "Soap_2" AS "soap_2",
    "Butter_2" AS "butter_2",
    "Soap_3" AS "soap_3",
    "Butter_3" AS "butter_3",
    "Occupation" AS "occupation",
    "Construction" AS "construction",
    "Construction_2" AS "construction_2",
    "Construction_3" AS "construction_3",
    "Construction_4" AS "construction_4",
    "c5"
FROM "gpih-mexico-1701-1813"
