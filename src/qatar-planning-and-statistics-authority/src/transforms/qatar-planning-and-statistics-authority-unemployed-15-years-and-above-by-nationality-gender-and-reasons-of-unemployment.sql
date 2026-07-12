-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "reason_of_unemployment",
    "sbb_lt_tl",
    "number_of_repetitions"
FROM "qatar-planning-and-statistics-authority-unemployed-15-years-and-above-by-nationality-gender-and-reasons-of-unemployment"
