-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "l_sr_w_dd_frd_l_sr",
    "number_of_households_and_members",
    "nw_lwhd",
    "type_of_unit",
    "nw_lskn",
    "resident_type",
    "value"
FROM "qatar-planning-and-statistics-authority-households-and-individuals-by-type-of-housing-unit-and-number-of-household-members"
