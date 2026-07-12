-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "educational_status",
    "lhl_lt_lymy",
    "count"
FROM "qatar-planning-and-statistics-authority-male-population-15-years-and-above-by-educational-status-and-age-groups"
