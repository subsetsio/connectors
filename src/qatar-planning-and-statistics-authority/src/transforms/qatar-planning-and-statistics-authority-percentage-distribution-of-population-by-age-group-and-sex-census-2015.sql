-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "lfy_t_l_mry",
    "males_number_dd_ldhkwr",
    "females_number_dd_lnth",
    "lnsb"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-population-by-age-group-and-sex-census-2015"
