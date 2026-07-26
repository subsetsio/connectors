-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "_location" AS location,
    "replacecurb",
    "replaceend",
    "replacebollard",
    "replaceanchor",
    "replaceclip",
    "replacearc",
    "replacepost",
    "repl_t_curb",
    "replacersb",
    "repaircurb",
    "repairend",
    "repairbollards",
    "repairpost",
    "repairrsb"
FROM "nyc-open-data-3f5t-9dqu"
