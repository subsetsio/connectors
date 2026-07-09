-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dispnum",
    "ord_incidnum",
    "stabb",
    "ccode",
    "stday",
    "stmon",
    "styear",
    "endday",
    "endmon",
    "endyear",
    "insidea",
    "sidea",
    "fatality",
    "fatalpre",
    "action",
    "hostlev",
    "revtype1",
    "revtype2",
    "version",
    "incidnum"
FROM "correlates-of-war-mid-incident-participant"
