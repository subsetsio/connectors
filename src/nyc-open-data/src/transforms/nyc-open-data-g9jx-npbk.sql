-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boroname",
    "borocode",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "stopname",
    "corner",
    "busstopid",
    "routes",
    "direction",
    "notes",
    "elected_official",
    "wo",
    "wireless_communication",
    "release_date",
    "rtpi_complete",
    "latitude",
    "longitude",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac",
    "_location" AS location
FROM "nyc-open-data-g9jx-npbk"
