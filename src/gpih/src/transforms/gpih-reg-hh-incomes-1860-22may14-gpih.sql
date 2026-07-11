-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "New England" AS "new_england",
    "422.54449006510004" AS "422_54449006510004",
    "69.40512208788999" AS "69_40512208788999",
    "51.867625870600016" AS "51_867625870600016",
    "46.11787899102993" AS "46_11787899102993",
    "97.98550514507942" AS "97_98550514507942",
    "589.9351172980695" AS "589_9351172980695",
    "New England_2" AS "new_england_2",
    "0.6673458099999657" AS "0_6673458099999657",
    "1077377.91" AS "1077377_91",
    "3.117770800000217" AS "3_117770800000217",
    "4.671896868582088" AS "4_671896868582088",
    "c12",
    "c13",
    "c14"
FROM "gpih-reg-hh-incomes-1860-22may14-gpih"
