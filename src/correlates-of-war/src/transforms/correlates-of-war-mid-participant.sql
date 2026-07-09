-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dispnum",
    "stabb",
    "ccode",
    "stday",
    "stmon",
    "styear",
    "endday",
    "endmon",
    "endyear",
    "sidea",
    "revstate",
    "revtype1",
    "revtype2",
    "fatality",
    "fatalpre",
    "hiact",
    "hostlev",
    "orig",
    "version"
FROM "correlates-of-war-mid-participant"
