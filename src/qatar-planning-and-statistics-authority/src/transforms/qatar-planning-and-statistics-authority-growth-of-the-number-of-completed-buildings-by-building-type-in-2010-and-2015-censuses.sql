-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_type",
    "nw_lmbn",
    "of_increase",
    "number_of_completed_building_2010_dd_lmbny_lmktml_2010",
    "number_of_completed_building_2015_dd_lmbny_lmktml_2015"
FROM "qatar-planning-and-statistics-authority-growth-of-the-number-of-completed-buildings-by-building-type-in-2010-and-2015-censuses"
