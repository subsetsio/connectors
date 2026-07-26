-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "mainstreet",
    "crossstree",
    "install_da",
    "long",
    "lat",
    "x",
    "y"
FROM "nyc-open-data-xc4v-ntf4"
