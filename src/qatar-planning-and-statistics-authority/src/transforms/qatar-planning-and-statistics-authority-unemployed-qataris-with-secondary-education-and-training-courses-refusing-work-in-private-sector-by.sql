-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "ljns",
    "reason",
    "lsbb",
    "number_of_repetitions"
FROM "qatar-planning-and-statistics-authority-unemployed-qataris-with-secondary-education-and-training-courses-refusing-work-in-private-sector-by"
