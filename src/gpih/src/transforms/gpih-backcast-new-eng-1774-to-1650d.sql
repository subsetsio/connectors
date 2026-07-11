-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "(NewEng.f)" AS neweng_f,
    "Slave retained incomes are assumed to be the same fraction o" AS slave_retained_incomes_are_assumed_to_be_the_same_fraction_o,
    "c0",
    "12.92715990448524" AS 12_92715990448524,
    "11.144677399685413" AS 11_144677399685413,
    "11.255206727193741" AS 11_255206727193741,
    "10.26347985490888" AS 10_26347985490888,
    "8.323046838923" AS 8_323046838923,
    "7.028746054117284" AS 7_028746054117284,
    "c7",
    "Boston free" AS boston_free,
    "115.44850886236226" AS 115_44850886236226,
    "142.6013130183742" AS 142_6013130183742,
    "119.07096372020716" AS 119_07096372020716,
    "110.03375527592199" AS 110_03375527592199,
    "110.50253020089478" AS 110_50253020089478,
    "118.50127975414033" AS 118_50127975414033,
    "NewEng.d, e" AS neweng_d_e,
    "c16",
    "Group 4A" AS group_4a,
    "Artisans (manufacturing trades)" AS artisans_manufacturing_trades,
    "614.0192837966974" AS 614_0192837966974,
    "17.864137932772312" AS 17_864137932772312,
    "Group 4A_2" AS group_4a_2,
    "Artisans (manufacturing trades)_2" AS artisans_manufacturing_trades_2,
    "11532.292173655907" AS 11532_292173655907,
    "6.240663070058623" AS 6_240663070058623,
    "6.316925213205735" AS 6_316925213205735,
    "tie",
    "35.526324758351265" AS 35_526324758351265,
    "percent",
    """Families""" AS families,
    "3343",
    "65779",
    "c3",
    "c4",
    """Families""_2" AS families_2,
    "52989",
    "(presumably free only)" AS presumably_free_only,
    "Journal of Family History 8:346-366." AS journal_of_family_history_8_346_366
FROM "gpih-backcast-new-eng-1774-to-1650d"
