-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "training_agency",
    "training_agency_ar",
    "qatari_males",
    "qatari_females",
    "non_qatari_males",
    "non_qatari_females",
    "no_of_centers",
    "no_of_training_programs",
    "no_of_trainers_males",
    "no_of_trainers_females"
FROM "qatar-planning-and-statistics-authority-trainees-by-nationality-gender-and-training-agency"
