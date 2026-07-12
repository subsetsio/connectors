-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_condition",
    "hl_lmbn",
    "2015",
    "2010",
    "percentage_increase"
FROM "qatar-planning-and-statistics-authority-the-growth-of-the-number-of-buildings-by-building-condition-2010-and-2015-censuses"
