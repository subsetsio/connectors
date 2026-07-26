-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "assemblydist",
    "address",
    "borough",
    "communityboard",
    "congressionaldist",
    "coundist",
    "gardenname",
    "juris",
    "multipolygon",
    "openhrsf",
    "openhrsm",
    "openhrssa",
    "openhrssu",
    "openhrsth",
    "openhrstu",
    "openhrsw",
    "parksid",
    "policeprecinct",
    "statesenatedist",
    "status",
    "zipcode",
    "bbl",
    "nta",
    "censustract",
    "lat",
    "lon",
    "crossstreets"
FROM "nyc-open-data-p78i-pat6"
