-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "university_degree",
    "nationality",
    "gender",
    "number_of_graduates_dd_lkhryjyn",
    "lnw",
    "ljnsy",
    "ldrj_l_lmy"
FROM "qatar-planning-and-statistics-authority-number-of-graduates-with-disabilities-by-academic-degree-nationality-and-gender"
