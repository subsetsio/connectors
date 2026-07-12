-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "lmw_shr",
    "june_2024",
    "july_2024",
    "august_2024",
    "september_2024",
    "october_2024",
    "november_2024"
FROM "qatar-planning-and-statistics-authority-climate-indicators-monthly"
