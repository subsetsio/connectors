-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "households_and_their_members",
    "households_and_their_members_ar",
    "1986",
    "1997",
    "2004",
    "2010",
    "2015",
    "annual_growth_rate_in_2010_and_2015"
FROM "qatar-planning-and-statistics-authority-increase-in-number-of-households-and-their-members-during-the-years-of-census-1986-2015"
