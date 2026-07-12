-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_ar",
    "indicator",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-private-centers-number-of-training-courses-and-number-of-trainees"
