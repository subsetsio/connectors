-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "dd_ljwy_z_lty_tm_tqdymh_lljht_lwtny_w_ldwly_no_of_awards_presented_to_national_or_international_bodi",
    "no_of_obtained_prizes_domestically",
    "no_of_obtained_prizes_internationally"
FROM "qatar-planning-and-statistics-authority-number-and-type-of-environmental-rewards-attained-by-district-cooling-service-providers"
