-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "gispropnum",
    "_location" AS location,
    "borough",
    "eapply",
    "comfortsta",
    "signname",
    "nys_assemb",
    "nys_senate",
    "us_congres",
    "shape_star",
    "shape_stle"
FROM "nyc-open-data-bvus-rxia"
