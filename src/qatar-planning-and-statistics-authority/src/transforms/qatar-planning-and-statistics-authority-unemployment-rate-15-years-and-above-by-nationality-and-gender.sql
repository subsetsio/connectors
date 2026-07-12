-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "jns",
    "year",
    "nationality",
    "jnsy",
    "total"
FROM "qatar-planning-and-statistics-authority-unemployment-rate-15-years-and-above-by-nationality-and-gender"
