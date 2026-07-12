-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "males",
    "females",
    "total",
    "sector",
    "sector_ar",
    "precentage",
    "age_of_retirement"
FROM "qatar-planning-and-statistics-authority-retirees-registered-in-pension-funds-and-systems-by-labor-sector-civil-military"
