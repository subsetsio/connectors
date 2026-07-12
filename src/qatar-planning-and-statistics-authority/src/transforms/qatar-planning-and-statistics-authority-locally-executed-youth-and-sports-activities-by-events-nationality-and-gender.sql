-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event",
    "event_ar",
    "no_of_activities_implemented",
    "qataris_males",
    "qataris_females",
    "qataris_total",
    "non_qataris_males",
    "non_qataris_females",
    "non_qataris_total",
    "total_males",
    "total_females",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-locally-executed-youth-and-sports-activities-by-events-nationality-and-gender"
