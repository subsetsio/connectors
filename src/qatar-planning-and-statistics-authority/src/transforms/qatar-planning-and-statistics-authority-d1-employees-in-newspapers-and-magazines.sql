-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "qataris_males",
    "qataris_females",
    "non_qataris_males",
    "non_qataris_females"
FROM "qatar-planning-and-statistics-authority-d1-employees-in-newspapers-and-magazines"
