-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_assistance",
    "type_of_assistance_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-qataris-benefiting-from-assistance-rendered-by-ministry-of-administrative-development-and-labor-and"
