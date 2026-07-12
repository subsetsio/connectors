-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "nationality",
    "gender",
    "type_of_disability",
    "number_of_people_with_disabilities_dd_l_frd_dhww_l_qt",
    "nw_l_q",
    "lnw",
    "ljnsy"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-people-registered-at-disabled-centers-by-nationality-gender-and1"
