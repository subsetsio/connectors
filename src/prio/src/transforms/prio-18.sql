-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: MIRPS rows are political-regime spells or intervals; avoid treating interval start dates as annual observations without expansion.
SELECT
    "gwno",
    "polid",
    "startd",
    "endd",
    "startnd",
    "endnd",
    "xconst",
    "xrec",
    "part",
    "status",
    "duration",
    "demindex",
    "dist001",
    "dist010",
    "dist011",
    "dist100",
    "dist101",
    "dist110",
    "dist111",
    "distmid",
    "mindist",
    "ourtype",
    "ourtype_ncaes",
    "sip2",
    "year",
    "sip2status",
    "sip2ysc",
    "sip2_previous",
    "stsetpolid",
    "stsetorig"
FROM "prio-18"
