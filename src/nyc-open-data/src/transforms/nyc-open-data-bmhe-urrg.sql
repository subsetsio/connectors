-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "ell_removals",
    "ell_principal",
    "ell_superintendent",
    "ell_expulsions",
    "nonell_removals",
    "nonell_principal",
    "nonell_superintendent",
    "nonell_expulsions"
FROM "nyc-open-data-bmhe-urrg"
