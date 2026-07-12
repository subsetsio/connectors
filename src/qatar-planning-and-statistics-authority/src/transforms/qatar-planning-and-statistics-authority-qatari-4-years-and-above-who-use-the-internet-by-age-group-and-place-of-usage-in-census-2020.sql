-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "fy_t_l_mr",
    "place_of_usage",
    "mkn_lstkhdm",
    "percentage_of_qatari_population",
    "qatari_population"
FROM "qatar-planning-and-statistics-authority-qatari-4-years-and-above-who-use-the-internet-by-age-group-and-place-of-usage-in-census-2020"
