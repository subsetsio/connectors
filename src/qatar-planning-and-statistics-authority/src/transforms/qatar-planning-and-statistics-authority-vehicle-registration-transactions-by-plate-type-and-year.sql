-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "plate_type",
    "nw_llwh",
    "transaction",
    "lm_ml",
    "total"
FROM "qatar-planning-and-statistics-authority-vehicle-registration-transactions-by-plate-type-and-year"
