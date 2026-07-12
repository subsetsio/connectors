-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lsn_year",
    "lrb_quarter",
    "lshhr_month",
    "hs4",
    "ltfsyl",
    "details",
    "dwl_lmqsd",
    "country_of_destinatoion",
    "quantity",
    "weight_kg",
    "value_qr"
FROM "qatar-planning-and-statistics-authority-qatar-export-statistics-2019-2024"
