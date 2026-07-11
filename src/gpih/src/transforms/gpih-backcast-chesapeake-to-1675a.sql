-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Group 1" AS group_1,
    "Officials, titled, professions" AS officials_titled_professions,
    "613.8714425681233" AS 613_8714425681233,
    "4.4498100554505635" AS 4_4498100554505635,
    "Group 1_2" AS group_1_2,
    "Officials, titled, professions_2" AS officials_titled_professions_2,
    "c6",
    "1878.4235524619555" AS 1878_4235524619555,
    "1.1605271528259014" AS 1_1605271528259014,
    "1.2899760933776656" AS 1_2899760933776656,
    "c0",
    "1674-1688" AS 1674_1688,
    "21.24021240212402" AS 21_24021240212402,
    "64.43378408375735" AS 64_43378408375735,
    "c1",
    "year 1774" AS year_1774,
    "c1770",
    "c1750",
    "c1725",
    "c1700",
    "c1675",
    "c8",
    "1774",
    "c1770_2",
    "c1750_2",
    "c1725_2",
    "c1700_2",
    "c1675_2",
    "Detailed notes (see ""Detailed notes"" worksheet)" AS detailed_notes_see_detailed_notes_worksheet
FROM "gpih-backcast-chesapeake-to-1675a"
