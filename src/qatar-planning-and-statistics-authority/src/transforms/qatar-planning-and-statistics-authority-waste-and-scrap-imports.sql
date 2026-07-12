-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "hs8",
    "details_of_hs8",
    "tfsyl_rmz_lt_rf_ljmrky",
    "weight_kg",
    "value_qar"
FROM "qatar-planning-and-statistics-authority-waste-and-scrap-imports"
