-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mjl_ltdryb",
    "field_of_training",
    "qatari_males",
    "qatari_females",
    "non_qatari_males",
    "non_qatari_females"
FROM "qatar-planning-and-statistics-authority-trainees-at-governmental-and-mixed-training-centers-by-nationality-gender-and-field-of-training"
