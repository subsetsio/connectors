-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "c0",
    "Amsterdam" AS amsterdam,
    "Delft" AS delft,
    "countryside",
    "vlekken",
    "income",
    "weighted",
    "Leiden" AS leiden,
    "income Leiden" AS income_leiden,
    "weighted_2",
    "c10",
    "Income_1" AS income_1,
    "Overall" AS overall,
    "1",
    "173440",
    "100",
    "17.344" AS 17_344,
    "46.90267640560647" AS 46_90267640560647,
    "14.687227430158611" AS 14_687227430158611,
    "46.90267640560647_2" AS 46_90267640560647_2,
    "14.687227430158611_2" AS 14_687227430158611_2,
    "15.109907785567573" AS 15_109907785567573
FROM "gpih-netherlands-1808-holland-1732-2"
