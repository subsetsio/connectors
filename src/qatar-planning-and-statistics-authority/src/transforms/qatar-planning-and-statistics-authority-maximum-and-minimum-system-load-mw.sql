-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "maximum_load_mw",
    "maximum_load_date_mm_dd_yyyy",
    "minimum_load_mw",
    "minimum_load_date_mm_dd_yyyy"
FROM "qatar-planning-and-statistics-authority-maximum-and-minimum-system-load-mw"
