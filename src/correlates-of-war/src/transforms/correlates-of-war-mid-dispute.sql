-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dispnum",
    "stday",
    "stmon",
    "styear",
    "endday",
    "endmon",
    "endyear",
    "outcome",
    "settle",
    "fatality",
    "fatalpre",
    "maxdur",
    "mindur",
    "hiact",
    "hostlev",
    "recip",
    "numa",
    "numb",
    "ongo2014",
    "version"
FROM "correlates-of-war-mid-dispute"
