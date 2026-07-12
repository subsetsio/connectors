-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nutrients_by_location",
    "lmgdhyt_hsb_lmwq",
    "value",
    "national_maximum_allowed",
    "year"
FROM "qatar-planning-and-statistics-authority-average-marine-acidity-ph-measured-at-agreed-suite-of-representative-sampling-stations0"
