-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "qatari_teams",
    "non_qatari_teams",
    "total_teams",
    "qatari_clubs",
    "non_qatari_clubs",
    "total_clubs",
    "qatari_total",
    "non_qatari_total",
    "total"
FROM "qatar-planning-and-statistics-authority-coaches-accredited-in-sport-federations-by-place-of-work-and-nationality"
