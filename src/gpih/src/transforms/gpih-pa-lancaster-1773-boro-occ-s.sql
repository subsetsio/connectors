-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "row ID" AS "row_id",
    "Surname" AS "surname",
    "First name" AS "first_name",
    "Occupation" AS "occupation",
    "entity type (LW)" AS "entity_type_lw",
    "poor",
    "code (LW)" AS "code_lw",
    "Group" AS "group",
    "Roll 15 (label on the film), alias PA Historical Roll #209.1" AS "roll_15_label_on_the_film_alias_pa_historical_roll_209_1",
    "c9",
    "Occupational grouping" AS "occupational_grouping",
    "Number" AS "number",
    "residents",
    "households",
    "Number_2" AS "number_2",
    "residents_2",
    "households_2"
FROM "gpih-pa-lancaster-1773-boro-occ-s"
