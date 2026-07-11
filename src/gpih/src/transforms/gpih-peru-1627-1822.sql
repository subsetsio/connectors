-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Location" AS location,
    "Arequipa" AS arequipa,
    "Arequipa_2" AS arequipa_2,
    "Cusco" AS cusco,
    "Arequipa_3" AS arequipa_3,
    "Arequipa_4" AS arequipa_4,
    "Cusco_2" AS cusco_2,
    "Arequipa_5" AS arequipa_5,
    "Arequipa_6" AS arequipa_6,
    "Arequipa_7" AS arequipa_7,
    "Arequipa_8" AS arequipa_8,
    "Cusco_3" AS cusco_3,
    "Cusco_4" AS cusco_4,
    "A requipa" AS a_requipa,
    "A requipa_2" AS a_requipa_2,
    "A requipa_3" AS a_requipa_3,
    "Commodity" AS commodity,
    "Paper" AS paper,
    "Rouen cloth" AS rouen_cloth,
    "Iron" AS iron,
    "Paper_2" AS paper_2,
    "Rouen cloth_2" AS rouen_cloth_2,
    "Iron_2" AS iron_2
FROM "gpih-peru-1627-1822"
