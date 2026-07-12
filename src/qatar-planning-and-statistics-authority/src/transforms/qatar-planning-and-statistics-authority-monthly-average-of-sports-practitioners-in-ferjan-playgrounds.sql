-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "sm_lml_b",
    "name_of_playground",
    "value"
FROM "qatar-planning-and-statistics-authority-monthly-average-of-sports-practitioners-in-ferjan-playgrounds"
