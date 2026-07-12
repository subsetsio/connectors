-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lhdth",
    "event",
    "ljnsy_ljnsy",
    "nationality",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-participants-in-local-youth-and-sports-activities-by-event-nationality-and-gender"
