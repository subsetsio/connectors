-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "training_center_type",
    "nw_lmrkz_ltdryby",
    "duration_of_training",
    "ftr_ltdryb",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-trainees-at-governmental-and-mixed-training-centers-according-to-gender-and-duration-of-training"
