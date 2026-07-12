-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lbldy",
    "municipality",
    "nw_bynt_l_sr",
    "type_of_household_data",
    "value"
FROM "qatar-planning-and-statistics-authority-distribution-of-the-number-of-households-and-their-members-by-municipality"
