-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lfy_t_l_mry",
    "age_groups",
    "gender",
    "jns",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-qatari-deaths-by-place-of-death-gender-and-age-groups"
