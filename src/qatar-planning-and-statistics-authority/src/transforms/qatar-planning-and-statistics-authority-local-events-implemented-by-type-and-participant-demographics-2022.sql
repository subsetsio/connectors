-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_type",
    "lf_lyt_hsb_lnw",
    "number_of_events_implemented",
    "qatari_male_participants",
    "qatari_female_participants",
    "non_qatari_male_participants",
    "non_qatari_female_participants"
FROM "qatar-planning-and-statistics-authority-local-events-implemented-by-type-and-participant-demographics-2022"
