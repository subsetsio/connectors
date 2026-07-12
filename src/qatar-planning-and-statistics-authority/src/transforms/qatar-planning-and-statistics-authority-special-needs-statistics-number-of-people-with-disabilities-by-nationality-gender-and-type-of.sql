-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "nationality",
    "gender",
    "type_of_difficulty",
    "number_of_people_with_difficulties",
    "nw_ls_wb",
    "lnw",
    "ljnsy"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-people-with-disabilities-by-nationality-gender-and-type-of"
