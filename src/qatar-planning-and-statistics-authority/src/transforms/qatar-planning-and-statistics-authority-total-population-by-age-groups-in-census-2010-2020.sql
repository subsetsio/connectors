-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "lfy_l_mry",
    "population",
    "population0"
FROM "qatar-planning-and-statistics-authority-total-population-by-age-groups-in-census-2010-2020"
