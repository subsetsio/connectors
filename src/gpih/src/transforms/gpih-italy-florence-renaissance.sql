-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Commodity:" AS "commodity",
    "Veal" AS "veal",
    "Ox" AS "ox",
    "Pork backbone" AS "pork_backbone",
    "Pork" AS "pork",
    "Sausage" AS "sausage",
    "Fish" AS "fish",
    "Veal_2" AS "veal_2",
    "Ox_2" AS "ox_2",
    "Pork backbone_2" AS "pork_backbone_2",
    "Pork_2" AS "pork_2",
    "Sausage_2" AS "sausage_2",
    "Fish_2" AS "fish_2",
    "Veal_3" AS "veal_3",
    "Ox_3" AS "ox_3",
    "Pork backbone_3" AS "pork_backbone_3",
    "Pork_3" AS "pork_3",
    "Sausage_3" AS "sausage_3",
    "Fish_3" AS "fish_3",
    "1310",
    "3.1" AS "3_1",
    "6.8" AS "6_8",
    "2.2109433962264156" AS "2_2109433962264156",
    "4.849811320754717" AS "4_849811320754717",
    "Year" AS "year",
    "soldi",
    "Florin" AS "florin",
    "per soldi" AS "per_soldi",
    "per denari" AS "per_denari"
FROM "gpih-italy-florence-renaissance"
