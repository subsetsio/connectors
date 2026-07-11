-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The March 2007 EU KLEMS raw release contains repeated observations at the natural country-industry-variable-year grain; aggregate or deduplicate deliberately before combining values.
SELECT
    "iso3",
    "var",
    "isic",
    "year",
    "value"
FROM "groningen-growth-and-development-centre-10.34894-cfvddy"
