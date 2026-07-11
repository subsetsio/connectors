-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "c0",
    "Amsterdam" AS "amsterdam",
    "Delft" AS "delft",
    "countryside",
    "vlekken",
    "income",
    "weighted",
    "Leiden" AS "leiden",
    "income Leiden" AS "income_leiden",
    "weighted_2",
    "c10",
    "Income_1" AS "income_1",
    "Overall" AS "overall",
    "group",
    "households",
    "population",
    "(guliders/yr)" AS "guliders_yr",
    "div. by mean" AS "div_by_mean",
    "(guilders)" AS "guilders",
    "population_2",
    "Top 1%:" AS "top_1",
    "13.7" AS "13_7",
    "2",
    "45414",
    "150",
    "6.8121" AS "6_8121",
    "12.281123998409896" AS "12_281123998409896",
    "5.768615197012423" AS "5_768615197012423",
    "59.18380040401637" AS "59_18380040401637",
    "20.455842627171034" AS "20_455842627171034",
    "8.712647751945426" AS "8_712647751945426",
    "Gini 1 =" AS "gini_1",
    "0.5633" AS "0_5633"
FROM "gpih-netherlands-1808-holland-1732"
