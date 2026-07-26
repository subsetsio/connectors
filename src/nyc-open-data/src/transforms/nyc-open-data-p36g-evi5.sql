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
    "_name" AS name,
    "locker_name",
    "locker_box_door",
    "locker_size",
    "address",
    "_location" AS location,
    "popupinfo",
    "latitude",
    "longitude",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac",
    "status"
FROM "nyc-open-data-p36g-evi5"
