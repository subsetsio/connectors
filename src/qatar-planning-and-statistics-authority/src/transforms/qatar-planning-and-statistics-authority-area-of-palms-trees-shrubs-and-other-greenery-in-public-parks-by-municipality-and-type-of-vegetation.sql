-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "item",
    "lbyn",
    "doha",
    "al_rayyan",
    "al_shamal",
    "al_wakra",
    "umm_salal",
    "al_khor",
    "al_daayen",
    "al_sheehaniya",
    "total"
FROM "qatar-planning-and-statistics-authority-area-of-palms-trees-shrubs-and-other-greenery-in-public-parks-by-municipality-and-type-of-vegetation"
