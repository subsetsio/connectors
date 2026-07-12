-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "qataris",
    "non_qataris"
FROM "qatar-planning-and-statistics-authority-mean-age-of-women-at-childbearing"
