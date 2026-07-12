-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_allowance",
    "gender",
    "nw_lbdl",
    "lnw",
    "value"
FROM "qatar-planning-and-statistics-authority-beneficiaries-of-social-security-servant-allowance-by-type-of-allowance-and-gender"
