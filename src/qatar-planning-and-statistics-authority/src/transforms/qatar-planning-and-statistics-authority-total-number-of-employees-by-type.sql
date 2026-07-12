-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "electricity_business",
    "water_business",
    "corporate_services"
FROM "qatar-planning-and-statistics-authority-total-number-of-employees-by-type"
