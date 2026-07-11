-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Location" AS "location",
    "Potosí" AS "potos",
    "Potosí_2" AS "potos_2",
    "Potosí_3" AS "potos_3",
    "Potosí_4" AS "potos_4",
    "Potosí_5" AS "potos_5",
    "Potosí_6" AS "potos_6",
    "Potosí_7" AS "potos_7",
    "Potosí_8" AS "potos_8",
    "Commodity" AS "commodity",
    "Sugar" AS "sugar",
    "Sugar_2" AS "sugar_2",
    "Cinnamon" AS "cinnamon",
    "Cinnamon_2" AS "cinnamon_2",
    "Sugar_3" AS "sugar_3",
    "Cinnamon_3" AS "cinnamon_3",
    "Sugar_4" AS "sugar_4",
    "Cinnamon_4" AS "cinnamon_4",
    "Paper" AS "paper",
    "Paper_2" AS "paper_2",
    "Rouen linen" AS "rouen_linen",
    "Rouen linen_2" AS "rouen_linen_2",
    "Coarse Cotton cloth" AS "coarse_cotton_cloth",
    "Coarse Cotton cloth_2" AS "coarse_cotton_cloth_2",
    "Soap" AS "soap",
    "Soap_2" AS "soap_2",
    "Paper_3" AS "paper_3",
    "Rouen linen_3" AS "rouen_linen_3",
    "Coarse Cotton cloth_3" AS "coarse_cotton_cloth_3",
    "Soap_3" AS "soap_3"
FROM "gpih-bolivia-1676-1816"
