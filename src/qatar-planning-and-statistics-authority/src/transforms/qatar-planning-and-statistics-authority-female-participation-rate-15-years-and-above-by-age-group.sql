-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups",
    "fy_t_l_mr",
    "total"
FROM "qatar-planning-and-statistics-authority-female-participation-rate-15-years-and-above-by-age-group"
