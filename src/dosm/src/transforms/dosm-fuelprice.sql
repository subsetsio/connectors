-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series_type",
    "date",
    "ron95",
    "ron97",
    "diesel",
    "diesel_eastmsia",
    "ron95_budi95",
    "ron95_skps",
    "diesel_skds",
    "diesel_budi"
FROM "dosm-fuelprice"
