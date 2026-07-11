-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Where:" AS where,
    "Provence" AS provence,
    "Provence_2" AS provence_2,
    "c3",
    "c4",
    "Provence_3" AS provence_3,
    "Provence_4" AS provence_4,
    "1450",
    "(Series" AS series,
    "(Series_2" AS series_2,
    "26.540476832222293" AS 26_540476832222293,
    "c5",
    "(Series_3" AS series_3,
    "(Series_4" AS series_4,
    "location",
    "Auvergne" AS auvergne,
    "national average" AS national_average,
    "content",
    "Auvergne_2" AS auvergne_2,
    "national average_2" AS national_average_2,
    "Lorraine" AS lorraine,
    "national average_3" AS national_average_3,
    "national average_4" AS national_average_4,
    "occupation",
    "master mason" AS master_mason,
    "unskilled day laborer" AS unskilled_day_laborer,
    "skilled building craftsman" AS skilled_building_craftsman,
    "unskilled day labor" AS unskilled_day_labor,
    "Ag per" AS ag_per,
    "master mason_2" AS master_mason_2,
    "unskilled day laborer_2" AS unskilled_day_laborer_2,
    "skilled building craftsman_2" AS skilled_building_craftsman_2,
    "unskilled day labor_2" AS unskilled_day_labor_2
FROM "gpih-france-1450-1789-non-paris"
