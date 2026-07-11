-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Battle-death measures include multiple estimate columns and conflict classifications; choose the intended estimate and conflict type before aggregation.
SELECT
    "id",
    "year",
    "bdeadlow",
    "bdeadhig",
    "bdeadbes",
    "annualdata",
    "source",
    "bdversion",
    "location",
    "sidea",
    "sidea2nd",
    "sideb",
    "sideb2nd",
    "incomp",
    "terr",
    "int",
    "cumint",
    "type",
    "startdate",
    "startprec",
    "startdate2",
    "startprec2",
    "epend",
    "ependdate",
    "ependprec",
    "gwnoa",
    "gwnoa2nd",
    "gwnob",
    "gwnob2nd",
    "gwnoloc",
    "region",
    "version"
FROM "prio-1"
