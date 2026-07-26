-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "carshare_c",
    "site_reque",
    "on_street",
    "from_" AS from,
    "_to" AS to,
    "address",
    "site_id",
    "community",
    "side",
    "borough",
    "lat",
    "long",
    "geom2"
FROM "nyc-open-data-wkij-g2bh"
