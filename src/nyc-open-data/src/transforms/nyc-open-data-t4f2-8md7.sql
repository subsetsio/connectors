-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borocode",
    "boroname",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "shelter_id",
    "corner",
    "on_street",
    "cross_stre",
    "longitude",
    "latitude",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-t4f2-8md7"
