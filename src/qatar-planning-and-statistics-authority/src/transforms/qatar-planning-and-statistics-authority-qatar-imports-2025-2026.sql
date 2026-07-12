-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "month",
    "hs12",
    "ltfsyl",
    "details",
    "dwl_lmnsh",
    "country_of_origin",
    "quantity",
    "weight_kg",
    "value_qr"
FROM "qatar-planning-and-statistics-authority-qatar-imports-2025-2026"
