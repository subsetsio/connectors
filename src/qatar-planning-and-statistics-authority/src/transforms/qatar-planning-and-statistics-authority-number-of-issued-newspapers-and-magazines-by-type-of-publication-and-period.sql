-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "newspapers_magazines",
    "newspapers_magazines_ar",
    "period",
    "period_ar",
    "year",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-issued-newspapers-and-magazines-by-type-of-publication-and-period"
