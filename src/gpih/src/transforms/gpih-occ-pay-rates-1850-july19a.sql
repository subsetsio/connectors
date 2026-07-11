-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "JGW, with the assistance of Oscar Méndez" AS "jgw_with_the_assistance_of_oscar_m_ndez",
    "New" AS "new",
    "Middle" AS "middle",
    "South" AS "south",
    "East" AS "east",
    "West" AS "west",
    "East_2" AS "east_2",
    "West_2" AS "west_2",
    "Mountain *" AS "mountain",
    "Pacific" AS "pacific",
    "* Note: There are no non-farm Mountain state observations fo" AS "note_there_are_no_non_farm_mountain_state_observations_fo",
    "c0",
    "Col. B" AS "col_b",
    "Col. C" AS "col_c",
    "Col. L" AS "col_l",
    "Col. M =" AS "col_m",
    "Col. N" AS "col_n",
    "Col. O" AS "col_o",
    "c7",
    "c8",
    "c9",
    "Domestic, female" AS "domestic_female",
    "0.909137918297998" AS "0_909137918297998",
    "0.921875" AS "0_921875",
    "1.1279137529137528" AS "1_1279137529137528",
    "0.7969924812030075" AS "0_7969924812030075",
    "1",
    "1_2",
    "1.282608695652174" AS "1_282608695652174",
    "1.5636864026140507" AS "1_5636864026140507",
    "1_3"
FROM "gpih-occ-pay-rates-1850-july19a"
