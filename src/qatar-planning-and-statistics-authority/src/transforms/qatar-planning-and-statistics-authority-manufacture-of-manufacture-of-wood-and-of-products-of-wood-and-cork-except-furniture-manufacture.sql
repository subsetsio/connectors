-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "license_type",
    "no_of_firms",
    "investment_qar_mil",
    "no_of_labour"
FROM "qatar-planning-and-statistics-authority-manufacture-of-manufacture-of-wood-and-of-products-of-wood-and-cork-except-furniture-manufacture"
