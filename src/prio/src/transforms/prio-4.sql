-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: UCDP/PRIO conflict records are conflict-year observations with dyad and incompatibility attributes; filter conflict type and intensity before aggregation.
-- caution: The raw extract contains an exact duplicate conflict-year row, so there is no source-stable row key.
SELECT
    "id",
    "location",
    "sidea",
    "sidea2nd",
    "sideb",
    "sideb2nd",
    "incomp",
    "terr",
    "year",
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
    "region"
FROM "prio-4"
