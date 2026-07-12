-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "college",
    "employed_academia",
    "employed_government",
    "employed_private",
    "employed_semi_government",
    "employed_total",
    "unemployed",
    "employment_rate",
    "higher_studies",
    "no_data_available",
    "total_graduated"
FROM "qatar-planning-and-statistics-authority-employment-rate-from-graduate-2023-24"
