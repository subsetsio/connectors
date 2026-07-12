-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lfy_t_l_mry_blsnwt",
    "age_groups_in_years",
    "lnw",
    "gender",
    "lhl_lzwjy",
    "marital_status",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-deaths-15-years-old-and-over-by-marital-status-gender-and-age-group"
