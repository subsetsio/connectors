-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Upper S Atl (Ches, WV)" AS upper_s_atl_ches_wv,
    "142653",
    "4.115812496056865" AS 4_115812496056865,
    "Slaves' retained earnings" AS slaves_retained_earnings,
    "c4",
    "16357149.180001313" AS 16357149_180001313,
    "114.66389897163967" AS 114_66389897163967,
    "South Atlantic, upper =" AS south_atlantic_upper,
    "50",
    "c9",
    "Missouri (WNC)" AS missouri_wnc,
    "2544323.2099999255" AS 2544323_2099999255,
    "89315.99999999999" AS 89315_99999999999,
    "20561.1" AS 20561_1,
    "58761",
    "43.29952196184417" AS 43_29952196184417,
    "86.59904392368836" AS 86_59904392368836,
    "c8",
    "Phillips" AS phillips,
    """Ave slave"" Bb212" AS ave_slave_bb212,
    "c11"
FROM "gpih-slave-retained-earnings-1850c-1860c"
