-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lfy_t_l_mry",
    "age_group",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-qatari-deaths-overseas-by-age-groups-and-gender"
