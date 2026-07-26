-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "ats_code",
    "loc_code",
    "loc_name",
    "managed_by",
    "lcc",
    "primarybui",
    "bin",
    "bbl",
    "address",
    "city",
    "boronum",
    "state",
    "zip",
    "geodistric",
    "adimindist",
    "xcoordinat",
    "ycoordinat"
FROM "nyc-open-data-a3nt-yts4"
