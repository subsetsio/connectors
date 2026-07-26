-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geoid",
    "countyfips",
    "borocode",
    "boroname",
    "boroct2020",
    "ct2020",
    "ctlabel",
    "ntacode",
    "ntatype",
    "ntaname",
    "ntaabbrev",
    "cdtacode",
    "cdtatype",
    "cdtaname"
FROM "nyc-open-data-hm78-6dwm"
