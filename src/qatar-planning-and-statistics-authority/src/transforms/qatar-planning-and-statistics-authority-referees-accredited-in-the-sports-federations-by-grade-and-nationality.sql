-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "international_qataris",
    "international_non_qataris",
    "first_qataris",
    "first_non_qataris",
    "second_qataris",
    "second_non_qataris",
    "third_qataris",
    "third_non_qataris"
FROM "qatar-planning-and-statistics-authority-referees-accredited-in-the-sports-federations-by-grade-and-nationality"
