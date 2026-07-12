-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lbyn",
    "annual_salary",
    "non_qatari_females",
    "non_qatari_males",
    "qatari_females",
    "qatari_males",
    "item"
FROM "qatar-planning-and-statistics-authority-employees-and-compensation-in-district-cooling-and-environmental-activities-by-nationality-and-gender-qr"
