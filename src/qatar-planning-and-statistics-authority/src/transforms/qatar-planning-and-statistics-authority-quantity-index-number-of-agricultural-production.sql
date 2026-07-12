-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "product",
    "lmntj",
    "quantity_index"
FROM "qatar-planning-and-statistics-authority-quantity-index-number-of-agricultural-production"
