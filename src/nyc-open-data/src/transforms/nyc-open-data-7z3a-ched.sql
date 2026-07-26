-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boroname",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "site_name",
    "street",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-7z3a-ched"
