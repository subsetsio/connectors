-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "municipality",
    "lbldy",
    "gender",
    "ljns",
    "qataris",
    "non_qataris",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-deaths-by-nationality-gender-and-municipality"
