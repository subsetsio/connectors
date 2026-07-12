-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality_place_of_wife",
    "lbldy_mkn_qm_lzwj",
    "nationality_wife",
    "ljnsy_lzwj",
    "value",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-marriages-by-nationality-and-place-of-wife"
