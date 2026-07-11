-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "1608",
    "0.064" AS "0_064",
    "1.15" AS "1_15",
    "17.96875" AS "17_96875",
    "0.2728292363734485" AS "0_2728292363734485",
    "6.9" AS "6_9",
    "25.290544707442145" AS "25_290544707442145",
    "1609",
    "0.47431110305865304" AS "0_47431110305865304",
    "3.5242" AS "3_5242",
    "7.4301444289913645" AS "7_4301444289913645",
    "0.025993883792048936" AS "0_025993883792048936",
    "1.266876" AS "1_266876",
    "48.737464941176455" AS "48_737464941176455",
    "c0",
    "Java" AS "java",
    "Amsterdam" AS "amsterdam",
    "Markup" AS "markup",
    "1623",
    "0.08746556473829202" AS "0_08746556473829202",
    "0.77" AS "0_77",
    "8.803464566929133" AS "8_803464566929133",
    "0.07083400000000001" AS "0_07083400000000001",
    "0.76388" AS "0_76388",
    "10.78408673800717" AS "10_78408673800717",
    "Malacca" AS "malacca",
    "Japan" AS "japan",
    "China (Canton)" AS "china_canton",
    "Bengal, China and Persia" AS "bengal_china_and_persia",
    "India (Coromandel)" AS "india_coromandel",
    "India (Bengal)" AS "india_bengal"
FROM "gpih-zwart-dutch-asiatic-p-1608-1800a"
