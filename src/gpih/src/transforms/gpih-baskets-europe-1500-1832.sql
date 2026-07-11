-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Bottom 40%, 1688 (King-R. Stone)" AS bottom_40_1688_king_r_stone,
    "c1",
    "8.528478483810952" AS 8_528478483810952,
    "21.321196209527383" AS 21_321196209527383,
    "6.716176806001126" AS 6_716176806001126,
    "11.193628010001877" AS 11_193628010001877,
    "5.223693071334209" AS 5_223693071334209,
    "59.69934938667667" AS 59_69934938667667,
    "6.294964729772907" AS 6_294964729772907,
    "15.91982650311378" AS 15_91982650311378,
    "13.767606441467024" AS 13_767606441467024,
    "0",
    "4.3182529389696125" AS 4_3182529389696125,
    "99.99999999999999" AS 99_99999999999999
FROM "gpih-baskets-europe-1500-1832"
