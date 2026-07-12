-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "lwhdt_lskny_lmshgwl_occupied_housing_units",
    "lwhdt_lskny_lmglq_closed_housing_units",
    "lwhdt_lskny_lkhly_vacant_housing_units",
    "ltwzy_lnsby",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-distribution-of-occupiedclosedvacant-units-in-2015-census"
