-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "parkorplayground",
    "date",
    "sportsplayed",
    "kimorsse",
    "attendance",
    "cancellation"
FROM "nyc-open-data-4pta-f4ca"
