-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "fy_t_l_mr_blsnwt",
    "age_groups_in_years",
    "lbldy",
    "municipality",
    "value",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-females-population-by-municipality-and-age-groups-december-2020"
