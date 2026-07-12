-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation",
    "lmhn",
    "age_group",
    "number"
FROM "qatar-planning-and-statistics-authority-economically-active-females-15-years-and-above-by-age-group-and-occupation"
