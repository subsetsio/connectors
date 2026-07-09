-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dispnum",
    "ord_incidnum",
    "stday",
    "stmon",
    "styear",
    "endday",
    "endmon",
    "endyear",
    "duration",
    "tbi",
    "fatality",
    "fatalpre",
    "action",
    "hostlev",
    "numa",
    "version",
    "incidnum"
FROM "correlates-of-war-mid-incident"
