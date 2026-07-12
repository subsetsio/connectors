-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_unit",
    "census_year",
    "value_type",
    "al_sheehaniya",
    "al_daayen",
    "al_shamal",
    "al_khor_al_thakira",
    "umm_slal",
    "al_wakra",
    "al_rayyan",
    "doha",
    "total"
FROM "qatar-planning-and-statistics-authority-housing-units-by-type-of-units-and-municipality-in-census-2010-2020"
