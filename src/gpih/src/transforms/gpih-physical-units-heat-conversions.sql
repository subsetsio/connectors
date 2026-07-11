-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "1 Wiener Elle = 0.778 m (in Bohemia from 1756 apparently)" AS 1_wiener_elle_0_778_m_in_bohemia_from_1756_apparently,
    "(says de.wiki.org)" AS says_de_wiki_org,
    "c2",
    "Beech, Blue (Ironwood)" AS beech_blue_ironwood,
    "Carpinus caroliniana" AS carpinus_caroliniana,
    "3825",
    "23.7" AS 23_7,
    "1",
    "0",
    "1_2",
    "c7"
FROM "gpih-physical-units-heat-conversions"
