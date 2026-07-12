-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mkn_ltwjd_lyl_lt_dd",
    "place_of_residency_on_census_night",
    "nw_lsr",
    "type_of_household",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-population-by-type-of-household-gender-and-place-of-residence-on-the-census-night-december-2020"
