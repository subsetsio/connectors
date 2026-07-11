-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-run WIOD uses source industry hierarchy fields; treat `isic3` and `isic3par` as release-specific industry codes.
SELECT
    "countrycode",
    "var",
    "isic3",
    "isic3par",
    "year",
    "value"
FROM "groningen-growth-and-development-centre-10.34894-a7axdn"
