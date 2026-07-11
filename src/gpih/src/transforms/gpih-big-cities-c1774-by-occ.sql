-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "professionals",
    "11 to 19" AS 11_to_19,
    "0.07" AS 0_07,
    "0.072" AS 0_072,
    "0.035" AS 0_035,
    "0.047" AS 0_047,
    "0.029" AS 0_029,
    "0.03" AS 0_03,
    "0.019" AS 0_019,
    "0.027" AS 0_027,
    "0.09902280130293159" AS 0_09902280130293159,
    "0.1130952380952381" AS 0_1130952380952381,
    "professionals_2",
    "11 to 19_2" AS 11_to_19_2,
    "0.035_2" AS 0_035_2,
    "c15",
    "0.03804347826086957" AS 0_03804347826086957,
    "0.05225752508361205" AS 0_05225752508361205,
    "0.07_2" AS 0_07_2,
    "0.07322175732217574" AS 0_07322175732217574,
    "0.08973254573796048" AS 0_08973254573796048,
    "0.019_2" AS 0_019_2,
    "0.01962809917355372" AS 0_01962809917355372,
    "0.033725256311947976" AS 0_033725256311947976,
    "Occupation" AS occupation,
    "LW code" AS lw_code,
    "count",
    "Shares" AS shares,
    "count_2",
    "Shares_2" AS shares_2,
    "count_3",
    "count excluding" AS count_excluding,
    "Shares, excl." AS shares_excl,
    "Shares, excl._2" AS shares_excl_2
FROM "gpih-big-cities-c1774-by-occ"
