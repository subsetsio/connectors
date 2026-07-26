-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "park_name",
    "width_ft",
    "_class" AS class,
    "surface",
    "gen_topog",
    "difficulty",
    "date_collected",
    "trail_name",
    "parkid",
    "trailmarkersinstalled",
    "shape"
FROM "nyc-open-data-vjbm-hsyr"
