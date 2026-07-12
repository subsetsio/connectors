-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_grade",
    "ldrj_lmly",
    "start_of_salary_range",
    "l_lw_ldwry",
    "periodic_increment",
    "nhy_lmrbwt",
    "end_of_salary_range"
FROM "qatar-planning-and-statistics-authority-aldrjat-alwzyfyh-wslm-alrwatb"
