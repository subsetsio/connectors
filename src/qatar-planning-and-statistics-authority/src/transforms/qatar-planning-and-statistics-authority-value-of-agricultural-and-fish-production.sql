-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "product_group",
    "mjmw_lmntj",
    "product",
    "lmntj",
    "value"
FROM "qatar-planning-and-statistics-authority-value-of-agricultural-and-fish-production"
