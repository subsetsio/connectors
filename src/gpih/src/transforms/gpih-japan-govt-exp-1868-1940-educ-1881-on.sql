-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "c0",
    "Central gov't" AS "central_gov_t",
    "Prefectures" AS "prefectures",
    "City, town, and Dörfe" AS "city_town_and_d_rfe",
    "All non-central" AS "all_non_central",
    "All levels of gov't" AS "all_levels_of_gov_t",
    "prod (GDP?) ¥1000s" AS "prod_gdp_1000s",
    "come ¥1000s" AS "come_1000s",
    "Central" AS "central",
    "All gov't" AS "all_gov_t",
    "exp in ¥1000s" AS "exp_in_1000s",
    "tures in ¥1000s" AS "tures_in_1000s",
    "in ¥1000s" AS "in_1000s",
    "ments in ¥1000s" AS "ments_in_1000s",
    "ments in ¥1000s_2" AS "ments_in_1000s_2",
    "1934-36 = 100" AS "1934_36_100",
    "in 1000s" AS "in_1000s_2"
FROM "gpih-japan-govt-exp-1868-1940-educ-1881-on"
