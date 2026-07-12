-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "number_of_residential_buildings_dd_lmbny_lskny",
    "of_residential_buildings_lmbny_lskny",
    "number_of_residential_commercial_buildings_dd_lmbny_lskny_ltjry",
    "of_residential_commercial_buildings_lmbny_lskny_ltjry",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-completed-buildings-residential-and-residentialcommercial-by-municipality-in-2015-census"
