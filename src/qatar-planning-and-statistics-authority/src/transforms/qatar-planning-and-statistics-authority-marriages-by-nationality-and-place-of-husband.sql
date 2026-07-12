-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lbldy_mkn_qm_lzwj",
    "municipality_place_of_husband",
    "ljnsy_lzwj",
    "nationality_husband",
    "total",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-marriages-by-nationality-and-place-of-husband"
