-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_date",
    "mode_of_transportation",
    "arrivals"
FROM "qatar-planning-and-statistics-authority-visitor-arrivals-trends-by-mode-of-transport-air-land-sea"
