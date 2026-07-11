-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: EU KLEMS release schemas and code domains differ across vintages; harmonize `var` and `isic` codes before combining releases.
SELECT
    "iso3",
    "var",
    "isic",
    "year",
    "value"
FROM "groningen-growth-and-development-centre-10.34894-cslwpd"
