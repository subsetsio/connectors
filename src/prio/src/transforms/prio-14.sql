-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Boundary records are dyadic border segments with date intervals; do not treat rows as independent country observations.
-- caution: The raw spreadsheet includes repeated header-like rows, so this raw extract has no stable row key.
SELECT
    "cw1",
    "cw2",
    "startdate",
    "sday",
    "smonth",
    "syear",
    "sdprecision",
    "enddate",
    "eday",
    "emonth",
    "eyear",
    "edprecision",
    "length_km",
    "historical_explanations",
    "usage_comments"
FROM "prio-14"
