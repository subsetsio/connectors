-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "type_of_mosque",
    "nw_lmsjd",
    "number"
FROM "qatar-planning-and-statistics-authority-number-and-types-of-mosques-according-to-municipality"
